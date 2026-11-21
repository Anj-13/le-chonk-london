"""Supabase-backed persistence store (``PERSISTENCE_BACKEND=supabase``).

Uses the official ``supabase`` Python SDK (sync client) and offloads every network
call with ``asyncio.to_thread`` so the FastAPI WebSocket loop is never blocked.
The service-role key is required here and must stay server-side; browsers use the
anon/publishable key and are constrained by RLS (see supabase/migrations/).

Dashboard runs are ad-hoc, so unless ``SUPABASE_PROJECT_ID``/``SUPABASE_SCENARIO_ID``
are given the store bootstraps one project (``SUPABASE_PROJECT_NAME``, default
"covid19-sim") owned by a dedicated service user (``SUPABASE_SERVICE_EMAIL``) and one
scenario per simulation type named "dashboard". Provision these explicitly in
production instead of relying on runtime bootstrap.
"""

from __future__ import annotations

import asyncio
import json
import os
import secrets
import threading
from datetime import datetime, timezone
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from .persistence import (
    PersistenceError,
    PersistenceStore,
    RunRecord,
    RUN_MODES,
    SIMULATION_TYPES,
    validate_choice,
    validate_events,
    validate_uuid,
)

DEFAULT_PROJECT_NAME = "covid19-sim"
DEFAULT_SCENARIO_NAME = "dashboard"
DEFAULT_SERVICE_EMAIL = "system@covid19-sim.local"
BATCH_SIZE = 500


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def supabase_config_from_env() -> dict:
    """Read Supabase settings from env; raise PersistenceError listing what is missing."""
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = (os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
           or os.environ.get("SUPABASE_SECRET_KEY") or "").strip()
    missing = []
    if not url:
        missing.append("SUPABASE_URL")
    if not key:
        missing.append("SUPABASE_SERVICE_ROLE_KEY")
    if missing:
        raise PersistenceError(
            "PERSISTENCE_BACKEND=supabase but missing env var(s): "
            + ", ".join(missing)
            + ". The service-role key is server-only; never ship it to browsers.")
    cfg: dict[str, Any] = {
        "url": url,
        "service_role_key": key,
        "simulation_type": os.environ.get("SIMULATION_TYPE", "prompt_injection"),
        "project_name": os.environ.get("SUPABASE_PROJECT_NAME", DEFAULT_PROJECT_NAME),
        "service_email": os.environ.get("SUPABASE_SERVICE_EMAIL", DEFAULT_SERVICE_EMAIL),
    }
    for env, cfg_key in (("SUPABASE_PROJECT_ID", "project_id"),
                         ("SUPABASE_SCENARIO_ID", "scenario_id")):
        if os.environ.get(env):
            cfg[cfg_key] = os.environ[env]
    if os.environ.get("SUPABASE_SERVICE_PASSWORD"):
        cfg["service_password"] = os.environ["SUPABASE_SERVICE_PASSWORD"]
    return cfg


class SupabaseStore(PersistenceStore):
    remote = True

    def __init__(self, *, url: str, service_role_key: str,
                 simulation_type: str = "prompt_injection",
                 project_id: str | None = None, scenario_id: str | None = None,
                 project_name: str = DEFAULT_PROJECT_NAME,
                 service_email: str = DEFAULT_SERVICE_EMAIL,
                 service_password: str | None = None,
                 batch_size: int = BATCH_SIZE, request_timeout: float = 30.0):
        if not url.startswith("https://"):
            raise PersistenceError(f"SUPABASE_URL must be an https URL, got {url!r}")
        if not service_role_key:
            raise PersistenceError("service_role_key is required (server-side only)")
        validate_choice(simulation_type, "simulation_type", SIMULATION_TYPES)
        if project_id is not None:
            validate_uuid(project_id, "SUPABASE_PROJECT_ID")
        if scenario_id is not None:
            validate_uuid(scenario_id, "SUPABASE_SCENARIO_ID")
        try:
            import supabase  # official SDK; imported lazily so local mode needs no dep
        except ImportError:
            raise PersistenceError(
                "the 'supabase' package is required for PERSISTENCE_BACKEND=supabase; "
                "install it with: pip install supabase") from None
        try:
            from supabase.lib.client_options import SyncClientOptions
            options = SyncClientOptions(postgrest_client_timeout=request_timeout)
        except Exception:
            options = None
        self.simulation_type = simulation_type
        self.batch_size = max(1, batch_size)
        self._project_id = project_id
        self._scenario_id = scenario_id
        self._project_name = project_name
        self._service_email = service_email
        self._service_password = service_password or secrets.token_urlsafe(24)
        try:
            self._client = supabase.create_client(url, service_role_key, options=options)
        except Exception as exc:
            raise PersistenceError("Could not initialize the Supabase client") from exc
        self._context_lock = threading.Lock()

    async def authenticate(self, token: str):
        from supabase_auth.errors import AuthApiError

        def verify():
            try:
                response = self._client.auth.get_user(token)
            except AuthApiError as exc:
                if exc.status in (400, 401, 403, 422):
                    return None
                raise
            return response.user if response else None

        return await self._call(verify)

    async def member_projects(self, user_id: str) -> list[str]:
        def go():
            query = self._table("project_members").select("project_id").eq("user_id", user_id)
            return [row["project_id"] for row in self._pages(query.order("project_id"))]
        return await self._call(go)

    async def can_mirror(self, user) -> bool:
        if self._project_id:
            return self._project_id in await self.member_projects(user.id)
        # Only the verified bootstrap identity may provision the default project.
        return bool(user.email_confirmed_at and user.email
                    and user.email.casefold() == self._service_email.casefold())

    @staticmethod
    def _pages(query):
        offset = 0
        while True:
            rows = query.range(offset, offset + 499).execute().data or []
            if not rows:
                return
            yield from rows
            offset += len(rows)

    # -- plumbing -------------------------------------------------------------
    async def _call(self, fn):
        """Run a blocking SDK call in a worker thread (never blocks the event loop)."""
        try:
            return await asyncio.to_thread(fn)
        except PersistenceError:
            raise
        except Exception as e:
            raise PersistenceError(f"supabase call failed: {e}") from e

    def _table(self, name: str):
        return self._client.table(name)

    # -- bootstrap: default project + scenario for ad-hoc dashboard runs -------
    def _service_user_id_sync(self) -> str:
        admin = self._client.auth.admin
        try:
            res = admin.create_user({"email": self._service_email,
                                     "password": self._service_password,
                                     "email_confirm": True})
            uid = getattr(res, "user", None) and getattr(res.user, "id", None)
            if uid:
                return uid
        except Exception:
            pass  # likely "already registered"; look the user up instead
        page = 1
        while users := admin.list_users(page=page, per_page=100):
            for user in users:
                if user.email and user.email.casefold() == self._service_email.casefold():
                    return user.id
            page += 1
        raise PersistenceError(
            f"could not find or create service user {self._service_email!r}; "
            "set SUPABASE_PROJECT_ID and SUPABASE_SCENARIO_ID to skip bootstrap")

    def _ensure_context_sync(self) -> tuple[str, str]:
        if self._project_id and self._scenario_id:
            return self._project_id, self._scenario_id
        uid = self._service_user_id_sync()
        if not self._project_id:
            res = (self._table("projects").select("id").eq("name", self._project_name)
                   .eq("owner_id", uid).order("id").limit(1).execute())
            rows = res.data or []
            if rows:
                self._project_id = rows[0]["id"]
            else:
                project_id = str(uuid5(NAMESPACE_URL, f"chonkvid/project/{uid}/{self._project_name}"))
                self._table("projects").upsert(
                    {"id": project_id, "name": self._project_name, "owner_id": uid},
                    on_conflict="id", ignore_duplicates=True).execute()
                self._project_id = project_id
        if not self._scenario_id:
            res = (self._table("scenarios").select("id")
                   .eq("project_id", self._project_id)
                   .eq("simulation_type", self.simulation_type)
                   .eq("name", DEFAULT_SCENARIO_NAME).order("id").limit(1).execute())
            rows = res.data or []
            if rows:
                self._scenario_id = rows[0]["id"]
            else:
                scenario_id = str(uuid5(
                    NAMESPACE_URL, f"chonkvid/scenario/{self._project_id}/{self.simulation_type}"))
                self._table("scenarios").upsert({
                    "id": scenario_id, "project_id": self._project_id,
                    "simulation_type": self.simulation_type,
                    "name": DEFAULT_SCENARIO_NAME, "config": {}},
                    on_conflict="id", ignore_duplicates=True).execute()
                self._scenario_id = scenario_id
        return self._project_id, self._scenario_id

    # -- protocol (sync internals, async wrappers) -----------------------------
    def _create_run_sync(self, *, mode, simulation_type, label, config,
                         model_metadata, scenario_id) -> str:
        validate_choice(mode, "mode", RUN_MODES)
        validate_choice(simulation_type, "simulation_type", SIMULATION_TYPES)
        with self._context_lock:
            project_id, scen_id = self._ensure_context_sync()
        row = {"scenario_id": scenario_id or scen_id, "project_id": project_id,
               "status": "pending", "mode": mode,
               "model_metadata": model_metadata or {}, "config": config or {}}
        res = self._table("simulation_runs").insert(row).execute()
        if not res.data:
            raise PersistenceError("create_run returned no row")
        return res.data[0]["id"]

    async def create_run(self, *, mode: str, simulation_type: str = "prompt_injection",
                         label: str = "", config: dict | None = None,
                         model_metadata: dict | None = None,
                         scenario_id: str | None = None) -> str:
        if scenario_id is not None:
            validate_uuid(scenario_id, "scenario_id")
        return await self._call(lambda: self._create_run_sync(
            mode=mode, simulation_type=simulation_type, label=label,
            config=config, model_metadata=model_metadata, scenario_id=scenario_id))

    def _transition_sync(self, run_id: str, **fields) -> None:
        validate_uuid(run_id, "run_id")
        res = self._table("simulation_runs").update(fields).eq("id", run_id).execute()
        if not res.data:
            raise PersistenceError(f"unknown run id {run_id!r}")

    async def mark_run_running(self, run_id: str) -> None:
        await self._call(lambda: self._transition_sync(
            run_id, status="running", started_at=_utcnow()))

    async def complete_run(self, run_id: str) -> None:
        await self._call(lambda: self._transition_sync(
            run_id, status="completed", completed_at=_utcnow()))

    async def fail_run(self, run_id: str, error_message: str) -> None:
        await self._call(lambda: self._transition_sync(
            run_id, status="failed", error_message=str(error_message)[:2000],
            completed_at=_utcnow()))

    def _append_events_sync(self, run_id: str, events: list[tuple[int, dict]]) -> None:
        validate_uuid(run_id, "run_id")
        batch = validate_events(events)
        rows = [{"run_id": run_id, "sequence_number": seq,
                 "tick": ev.get("tick"), "event_type": ev["type"], "payload": json.loads(json.dumps(ev))}
                for seq, ev in batch]
        for i in range(0, len(rows), self.batch_size):
            chunk = rows[i:i + self.batch_size]
            try:
                self._table("simulation_events").upsert(
                    chunk, on_conflict="run_id,sequence_number", ignore_duplicates=True
                ).execute()
                # A retry is valid only if the persisted event is identical.
                query = (self._table("simulation_events")
                         .select("sequence_number,tick,event_type,payload")
                         .eq("run_id", run_id)
                         .in_("sequence_number", [row["sequence_number"] for row in chunk])
                         .order("sequence_number"))
                stored = list(self._pages(query))
                expected = [{k: v for k, v in row.items() if k != "run_id"} for row in chunk]
                if sorted(stored, key=lambda row: row["sequence_number"]) != expected:
                    raise PersistenceError("event sequence already exists with different content or is missing")
            except Exception as e:
                msg = str(e)
                if "23505" in msg or "duplicate" in msg.lower():
                    raise PersistenceError(
                        f"duplicate sequence_number for run {run_id} "
                        f"(unique constraint on (run_id, sequence_number))") from e
                raise PersistenceError(f"append_events failed: {msg}") from e

    async def append_events(self, run_id: str,
                            events: list[tuple[int, dict]]) -> None:
        await self._call(lambda: self._append_events_sync(run_id, events))

    def _row_to_record(self, row: dict) -> RunRecord:
        return RunRecord(
            run_id=row["id"], status=row.get("status", "unknown"),
            mode=row.get("mode", "mock"),
            simulation_type=(row.get("scenarios") or {}).get("simulation_type",
                                                             self.simulation_type)
            if isinstance(row.get("scenarios"), dict) else self.simulation_type,
            label=row.get("legacy_run_id") or "", scenario_id=row.get("scenario_id"), project_id=row.get("project_id"),
            config=row.get("config") or {}, model_metadata=row.get("model_metadata") or {},
            error_message=row.get("error_message"), created_at=row.get("created_at"),
            started_at=row.get("started_at"), completed_at=row.get("completed_at"))

    async def get_run(self, run_id: str, *, project_ids: list[str] | None = None) -> RunRecord | None:
        validate_uuid(run_id, "run_id")

        def go():
            if project_ids == []:
                return None
            query = self._table("simulation_runs").select("*,scenarios(simulation_type)").eq("id", run_id)
            if project_ids is not None:
                query = query.in_("project_id", project_ids)
            res = query.limit(1).execute()
            if not res.data:
                if project_ids is not None:
                    return None
                raise PersistenceError(f"unknown run id {run_id!r}")
            return self._row_to_record(res.data[0])
        return await self._call(go)

    async def list_runs(self, limit: int = 60, *, project_ids: list[str] | None = None) -> list[RunRecord]:
        def go():
            if project_ids == []:
                return []
            query = self._table("simulation_runs").select("*,scenarios(simulation_type)")
            if project_ids is not None:
                query = query.in_("project_id", project_ids)
            res = query.order("created_at", desc=True).limit(max(1, limit)).execute()
            return [self._row_to_record(r) for r in (res.data or [])]
        return await self._call(go)

    async def get_run_events(self, run_id: str) -> list[dict]:
        validate_uuid(run_id, "run_id")

        def go():
            query = (self._table("simulation_events")
                     .select("sequence_number,tick,event_type,payload")
                     .eq("run_id", run_id).order("sequence_number"))
            events = []
            for row in self._pages(query):
                payload = row.get("payload") or {}
                ev = dict(payload)
                ev["sequence_number"] = row["sequence_number"]
                ev.setdefault("type", row.get("event_type"))
                if row.get("tick") is not None:
                    ev.setdefault("tick", row["tick"])
                events.append(ev)
            return events
        return await self._call(go)

    async def legacy_run_id(self, project_id, filename):
        def fetch():
            rows = (self._table("simulation_runs").select("id").eq("project_id", project_id)
                    .eq("legacy_run_id", filename).limit(1).execute().data)
            return rows[0]["id"] if rows else None
        return await self._call(fetch)

    async def latest_report(self, project_id, kind):
        def fetch():
            rows = (self._table("simulation_reports").select("body")
                    .eq("project_id", project_id).eq("kind", kind)
                    .order("created_at", desc=True).order("id", desc=True).limit(1).execute().data)
            return rows[0]["body"] if rows else None
        return await self._call(fetch)

    async def save_report(self, project_id, kind, body):
        await self._call(lambda: self._table("simulation_reports").insert(
            {"project_id": project_id, "kind": kind, "body": body}).execute())

    async def save_result(self, run_id: str, metrics: dict,
                          report_path: str | None = None) -> None:
        validate_uuid(run_id, "run_id")
        if not isinstance(metrics, dict):
            raise PersistenceError("metrics must be a dict")

        def go():
            self._table("simulation_results").upsert(
                {"run_id": run_id, "metrics": metrics, "report_path": report_path},
                on_conflict="run_id").execute()
        await self._call(go)
