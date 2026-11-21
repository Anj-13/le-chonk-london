"""Optional Supabase / Postgres persistence for experiment results and run recordings.

Set DATABASE_URL in .env (sslmode=require for Supabase). When unset, all I/O stays on disk.
"""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from typing import Any, Iterator
from urllib.parse import quote_plus

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS chonkvid_results (
    id BIGSERIAL PRIMARY KEY,
    kind TEXT NOT NULL,
    is_latest BOOLEAN NOT NULL DEFAULT FALSE,
    body JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS chonkvid_results_latest_kind
    ON chonkvid_results (kind) WHERE is_latest;

CREATE TABLE IF NOT EXISTS chonkvid_runs (
    run_id TEXT PRIMARY KEY,
    label TEXT,
    event_count INT NOT NULL DEFAULT 0,
    body JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS chonkvid_runs_created_at ON chonkvid_runs (created_at DESC);
"""


def database_url() -> str:
    url = os.environ.get("DATABASE_URL", "").strip()
    if url:
        return url
    host = os.environ.get("SUPABASE_DB_HOST", "").strip()
    password = os.environ.get("SUPABASE_DB_PASSWORD", "").strip()
    if not host or not password:
        return ""
    user = os.environ.get("SUPABASE_DB_USER", "postgres").strip()
    database = os.environ.get("SUPABASE_DB_NAME", "postgres").strip()
    port = os.environ.get("SUPABASE_DB_PORT", "5432").strip()
    pw = quote_plus(password)
    return f"postgresql://{user}:{pw}@{host}:{port}/{database}?sslmode=require"


def enabled() -> bool:
    return bool(database_url())


def _psycopg():
    try:
        import psycopg  # type: ignore
        from psycopg.rows import dict_row  # type: ignore
    except ImportError as e:
        raise RuntimeError("Install psycopg: pip install 'psycopg[binary]>=3.2'") from e
    return psycopg, dict_row


@contextmanager
def connect() -> Iterator[Any]:
    psycopg, dict_row = _psycopg()
    with psycopg.connect(database_url(), row_factory=dict_row) as conn:
        yield conn


def init_schema() -> None:
    if not enabled():
        raise RuntimeError("DATABASE_URL (or SUPABASE_DB_* parts) is not set in .env")
    with connect() as conn:
        conn.execute(SCHEMA_SQL)
        conn.commit()


def check() -> dict[str, Any]:
    if not enabled():
        return {"ok": False, "error": "DATABASE_URL not configured"}
    with connect() as conn:
        row = conn.execute("SELECT current_database() AS db, version() AS version").fetchone()
        tables = conn.execute(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name LIKE 'chonkvid_%'
            ORDER BY 1
            """
        ).fetchall()
    return {
        "ok": True,
        "database": row["db"],
        "version": row["version"].split(",")[0],
        "tables": [t["table_name"] for t in tables],
    }


def upsert_latest(kind: str, body: dict) -> None:
    if not enabled():
        return
    payload = json.loads(json.dumps(body))
    with connect() as conn:
        conn.execute(
            "UPDATE chonkvid_results SET is_latest = FALSE WHERE kind = %s AND is_latest",
            (kind,),
        )
        conn.execute(
            """
            INSERT INTO chonkvid_results (kind, is_latest, body)
            VALUES (%s, TRUE, %s::jsonb)
            """,
            (kind, json.dumps(payload)),
        )
        conn.commit()


def get_latest(kind: str) -> dict | None:
    if not enabled():
        return None
    with connect() as conn:
        row = conn.execute(
            """
            SELECT body FROM chonkvid_results
            WHERE kind = %s AND is_latest
            ORDER BY id DESC LIMIT 1
            """,
            (kind,),
        ).fetchone()
    if not row:
        return None
    return row["body"]


def save_run(run_id: str, events: list[dict], label: str = "") -> None:
    if not enabled():
        return
    payload = json.loads(json.dumps(events))
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO chonkvid_runs (run_id, label, event_count, body)
            VALUES (%s, %s, %s, %s::jsonb)
            ON CONFLICT (run_id) DO UPDATE SET
                label = EXCLUDED.label,
                event_count = EXCLUDED.event_count,
                body = EXCLUDED.body
            """,
            (run_id, label or run_id, len(events), json.dumps(payload)),
        )
        conn.commit()


def list_runs(limit: int = 60) -> list[dict]:
    if not enabled():
        return []
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT run_id AS id, event_count, created_at,
                   octet_length(body::text) AS bytes
            FROM chonkvid_runs
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_run(run_id: str) -> list[dict] | None:
    if not enabled():
        return None
    with connect() as conn:
        row = conn.execute(
            "SELECT body FROM chonkvid_runs WHERE run_id = %s",
            (run_id,),
        ).fetchone()
    if not row:
        return None
    return row["body"]


def sync_run_file(path) -> None:
    """Upload a finished JSONL recording from disk."""
    if not enabled() or not path.exists():
        return
    events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not events:
        return
    label = path.stem
    save_run(path.name, events, label=label)