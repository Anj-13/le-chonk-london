"""Optional persistence backends for simulation runs.

Two interchangeable stores behind one async protocol:

- ``LocalStore`` (default, ``PERSISTENCE_BACKEND=local``): the existing JSONL
  recordings under ``runs/`` plus a small sidecar meta file per run. This is the
  current behavior and the replay contract (``/api/runs``, ``/api/runs/{id}``)
  is unchanged.
- ``SupabaseStore`` (``PERSISTENCE_BACKEND=supabase``, see ``supabase_store.py``):
  persistent runs/events/results in Supabase. The server mirrors every WebSocket
  run to Supabase *in addition to* the local JSONL recording, so local replay
  keeps working and persistence failures are reported, never silent.

All store methods are async; blocking SDK calls are offloaded by the Supabase
store, so the WebSocket event loop is never blocked.
"""

from __future__ import annotations

import json
import os
import re
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .experiment import RESULTS, RUNS

SIMULATION_TYPES = ("prompt_injection", "disease_outbreak")
RUN_STATUSES = ("pending", "running", "completed", "failed")
RUN_MODES = ("mock", "live")

_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)


class PersistenceError(RuntimeError):
    """Raised for invalid input or backend failures. Never swallowed silently."""


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_uuid(value: Any, name: str) -> str:
    if not isinstance(value, str) or not _UUID_RE.match(value):
        raise PersistenceError(f"{name} must be a UUID string, got {value!r}")
    return value


def validate_choice(value: Any, name: str, allowed: tuple[str, ...]) -> str:
    if value not in allowed:
        raise PersistenceError(f"{name} must be one of {allowed}, got {value!r}")
    return value


def validate_events(events: Iterable) -> list[tuple[int, dict]]:
    """Normalize ``[(sequence_number, event_dict), ...]`` and reject bad shapes."""
    out: list[tuple[int, dict]] = []
    for item in events:
        try:
            seq, ev = item
        except (TypeError, ValueError):
            raise PersistenceError(
                "append_events expects (sequence_number, event) pairs, "
                f"got {item!r}") from None
        if not isinstance(seq, int) or isinstance(seq, bool) or seq < 0:
            raise PersistenceError(f"sequence_number must be a non-negative int, got {seq!r}")
        if not isinstance(ev, dict) or not isinstance(ev.get("type"), str):
            raise PersistenceError(f"event at sequence {seq} must be a dict with a 'type' string")
        out.append((seq, ev))
    seqs = [s for s, _ in out]
    if len(set(seqs)) != len(seqs):
        raise PersistenceError(f"duplicate sequence_number in batch: {sorted(seqs)}")
    if seqs != sorted(seqs):
        raise PersistenceError(f"sequence numbers in batch must be ascending, got {seqs}")
    return out


@dataclass
class RunRecord:
    run_id: str
    status: str
    mode: str
    simulation_type: str = "prompt_injection"
    scenario_id: str | None = None
    project_id: str | None = None
    label: str = ""
    config: dict = field(default_factory=dict)
    model_metadata: dict = field(default_factory=dict)
    error_message: str | None = None
    created_at: str | None = None
    started_at: str | None = None
    completed_at: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


class PersistenceStore(ABC):
    """Async persistence protocol. ``remote`` distinguishes Supabase from local."""

    remote: bool = False

    @abstractmethod
    async def create_run(self, *, mode: str, simulation_type: str = "prompt_injection",
                         label: str = "", config: dict | None = None,
                         model_metadata: dict | None = None,
                         scenario_id: str | None = None) -> str:
        """Create a pending run; return its run id."""

    @abstractmethod
    async def mark_run_running(self, run_id: str) -> None: ...

    @abstractmethod
    async def append_events(self, run_id: str,
                            events: list[tuple[int, dict]]) -> None:
        """Append events in order; duplicate/out-of-order sequence numbers raise."""

    @abstractmethod
    async def complete_run(self, run_id: str) -> None: ...

    @abstractmethod
    async def fail_run(self, run_id: str, error_message: str) -> None: ...

    @abstractmethod
    async def get_run(self, run_id: str) -> RunRecord: ...

    @abstractmethod
    async def list_runs(self, limit: int = 60) -> list[RunRecord]: ...

    @abstractmethod
    async def get_run_events(self, run_id: str) -> list[dict]:
        """Return events in deterministic sequence order, each with 'sequence_number'."""

    @abstractmethod
    async def save_result(self, run_id: str, metrics: dict,
                          report_path: str | None = None) -> None: ...


class LocalStore(PersistenceStore):
    """File-backed store: the existing JSONL recordings + a per-run meta sidecar.

    The run id is the recording filename (``<stamp>-<label>.jsonl``), exactly what
    ``/api/runs`` lists and ``/api/runs/{run_id}`` replays, so the dashboard contract
    is unchanged. Status lives in ``<run_id>.meta.json`` sidecars, which the replay
    endpoint never reads (it only globs ``*.jsonl``).
    """

    remote = False

    def __init__(self, runs_dir: Path | None = None, results_dir: Path | None = None):
        self.runs_dir = Path(runs_dir) if runs_dir else RUNS
        self.results_dir = Path(results_dir) if results_dir else RESULTS

    # -- helpers ------------------------------------------------------------
    def _events_path(self, run_id: str) -> Path:
        if not run_id.endswith(".jsonl") or "/" in run_id or "\\" in run_id:
            raise PersistenceError(f"invalid local run id {run_id!r}")
        return self.runs_dir / run_id

    def _meta_path(self, run_id: str) -> Path:
        return self.runs_dir / f"{run_id}.meta.json"

    def _read_meta(self, run_id: str) -> dict:
        p = self._meta_path(run_id)
        if p.exists():
            return json.loads(p.read_text())
        if self._events_path(run_id).exists():
            return {"run_id": run_id, "status": "completed", "mode": "mock",
                    "simulation_type": "prompt_injection", "last_sequence": None}
        raise PersistenceError(f"unknown run id {run_id!r}")

    def _write_meta(self, meta: dict) -> None:
        meta["updated_at"] = _utcnow()
        self._meta_path(meta["run_id"]).write_text(json.dumps(meta))

    # -- protocol -----------------------------------------------------------
    async def create_run(self, *, mode: str, simulation_type: str = "prompt_injection",
                         label: str = "", config: dict | None = None,
                         model_metadata: dict | None = None,
                         scenario_id: str | None = None) -> str:
        validate_choice(mode, "mode", RUN_MODES)
        validate_choice(simulation_type, "simulation_type", SIMULATION_TYPES)
        if scenario_id is not None:
            validate_uuid(scenario_id, "scenario_id")
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        run_id = f"{stamp}-{label or 'run'}.jsonl"
        # Same name shape as experiment.Recorder.
        self._events_path(run_id).touch()
        self._write_meta({"run_id": run_id, "status": "pending", "mode": mode,
                          "simulation_type": simulation_type, "label": label,
                          "config": config or {}, "model_metadata": model_metadata or {},
                          "created_at": _utcnow(), "last_sequence": -1})
        return run_id

    async def mark_run_running(self, run_id: str) -> None:
        meta = self._read_meta(run_id)
        if meta["status"] != "pending":
            raise PersistenceError(f"run {run_id} is {meta['status']}, expected pending")
        meta["status"] = "running"
        meta["started_at"] = _utcnow()
        self._write_meta(meta)

    async def append_events(self, run_id: str,
                            events: list[tuple[int, dict]]) -> None:
        batch = validate_events(events)
        meta = self._read_meta(run_id)
        if meta["status"] not in ("running", "pending"):
            raise PersistenceError(f"run {run_id} is {meta['status']}; cannot append events")
        last = meta.get("last_sequence")
        if last is not None and batch and batch[0][0] <= last:
            raise PersistenceError(
                f"duplicate or out-of-order sequence_number for run {run_id}: "
                f"last={last}, first new={batch[0][0]}")
        with self._events_path(run_id).open("a") as f:
            for _, ev in batch:
                f.write(json.dumps(ev) + "\n")
        meta["last_sequence"] = batch[-1][0] if batch else last
        self._write_meta(meta)

    async def complete_run(self, run_id: str) -> None:
        meta = self._read_meta(run_id)
        meta["status"] = "completed"
        meta["completed_at"] = _utcnow()
        self._write_meta(meta)

    async def fail_run(self, run_id: str, error_message: str) -> None:
        meta = self._read_meta(run_id)
        meta["status"] = "failed"
        meta["error_message"] = str(error_message)[:2000]
        meta["completed_at"] = _utcnow()
        self._write_meta(meta)

    async def get_run(self, run_id: str) -> RunRecord:
        meta = self._read_meta(run_id)
        return RunRecord(run_id=run_id, status=meta.get("status", "unknown"),
                         mode=meta.get("mode", "mock"),
                         simulation_type=meta.get("simulation_type", "prompt_injection"),
                         label=meta.get("label", ""), config=meta.get("config") or {},
                         model_metadata=meta.get("model_metadata") or {},
                         error_message=meta.get("error_message"),
                         created_at=meta.get("created_at"),
                         started_at=meta.get("started_at"),
                         completed_at=meta.get("completed_at"))

    async def list_runs(self, limit: int = 60) -> list[RunRecord]:
        if not self.runs_dir.exists():
            return []
        files = sorted(self.runs_dir.glob("*.jsonl"), reverse=True)[: max(1, limit)]
        out = []
        for f in files:
            try:
                out.append(await self.get_run(f.name))
            except PersistenceError:
                continue
        return out

    async def get_run_events(self, run_id: str) -> list[dict]:
        p = self._events_path(run_id)
        if not p.exists():
            raise PersistenceError(f"unknown run id {run_id!r}")
        events = []
        for i, line in enumerate(p.read_text().splitlines()):
            if line.strip():
                ev = json.loads(line)
                ev["sequence_number"] = i
                events.append(ev)
        return events

    async def save_result(self, run_id: str, metrics: dict,
                          report_path: str | None = None) -> None:
        if not isinstance(metrics, dict):
            raise PersistenceError("metrics must be a dict")
        self._read_meta(run_id)  # raises for unknown runs
        out_dir = self.results_dir / "runs"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{run_id}.json").write_text(json.dumps(
            {"run_id": run_id, "metrics": metrics, "report_path": report_path,
             "saved_at": _utcnow()}, indent=2))


_STORE: PersistenceStore | None = None


def get_store() -> PersistenceStore:
    """Return the configured store (cached). Raises PersistenceError on bad config."""
    global _STORE
    if _STORE is not None:
        return _STORE
    backend = os.environ.get("PERSISTENCE_BACKEND", "local").strip().lower()
    if backend == "local":
        _STORE = LocalStore()
    elif backend == "supabase":
        from .supabase_store import SupabaseStore, supabase_config_from_env
        _STORE = SupabaseStore(**supabase_config_from_env())
    else:
        raise PersistenceError(
            f"PERSISTENCE_BACKEND must be 'local' or 'supabase', got {backend!r}")
    return _STORE


def reset_store() -> None:
    """Drop the cached store (used by tests after changing env vars)."""
    global _STORE
    _STORE = None
