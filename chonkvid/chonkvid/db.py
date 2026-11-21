"""Optional Supabase / Postgres persistence for experiment results and run recordings.

Set DATABASE_URL in .env (sslmode=require for Supabase). When unset, all I/O stays on disk.
"""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from typing import Any, Iterator
from urllib.parse import quote


def database_url() -> str:
    url = (
        os.environ.get("DATABASE_URL") or os.environ.get("SUPABASE_DB_URL", "")
    ).strip()
    if url:
        return url
    host = os.environ.get("SUPABASE_DB_HOST", "").strip()
    password = os.environ.get("SUPABASE_DB_PASSWORD", "").strip()
    if not host or not password:
        return ""
    user = os.environ.get("SUPABASE_DB_USER", "postgres").strip()
    database = os.environ.get("SUPABASE_DB_NAME", "postgres").strip()
    port = os.environ.get("SUPABASE_DB_PORT", "5432").strip()
    pw = quote(password, safe="")
    return f"postgresql://{user}:{pw}@{host}:{port}/{database}?sslmode=require"


def enabled() -> bool:
    return os.environ.get("PERSISTENCE_BACKEND", "local") == "supabase" and bool(
        database_url()
    )


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
    url = database_url()
    if not url:
        raise RuntimeError("Configure DATABASE_URL for shared SQL access")
    with psycopg.connect(url, row_factory=dict_row) as conn:
        yield conn


def check() -> dict[str, Any]:
    with connect() as conn:
        row = conn.execute(
            "select current_database() as db, version() as version"
        ).fetchone()
        names = [
            "simulation_runs",
            "simulation_events",
            "simulation_results",
            "simulation_reports",
        ]
        tables = conn.execute(
            "select table_name from information_schema.tables where table_schema='public' and table_name=any(%s)",
            (names,),
        ).fetchall()
        return {
            "ok": len(tables) == len(names),
            "database": row["db"],
            "version": row["version"],
            "tables": [t["table_name"] for t in tables],
            "error": "Apply the Supabase migrations first",
        }


def import_run(conn, project, scenario, filename, events, created_at=None):
    from psycopg.types.json import Jsonb

    if not events or events[0].get("source") not in ("mock", "live"):
        raise ValueError(f"Cannot determine recording mode for {filename}")
    row = conn.execute(
        """insert into simulation_runs
        (project_id,scenario_id,legacy_run_id,config,mode,created_at)
        values (%s,%s,%s,%s,%s,coalesce(%s,now()))
        on conflict(project_id,legacy_run_id) do nothing returning id""",
        (
            project,
            scenario,
            filename,
            Jsonb(events[0].get("config", {})),
            events[0]["source"],
            created_at,
        ),
    ).fetchone()
    if not row:
        existing = conn.execute(
            """select e.payload from simulation_events e join simulation_runs r on r.id=e.run_id
            where r.project_id=%s and r.scenario_id=%s and r.legacy_run_id=%s order by sequence_number""",
            (project, scenario, filename),
        ).fetchall()
        if [e["payload"] for e in existing] != events:
            raise ValueError(f"Existing recording differs for {filename}")
        return
    rid = row["id"]
    with conn.cursor() as cur:
        cur.executemany(
            """insert into simulation_events(run_id,sequence_number,event_type,tick,payload)
            values (%s,%s,%s,%s,%s)""",
            [
                (rid, i, ev["type"], ev.get("tick"), Jsonb(ev))
                for i, ev in enumerate(events)
            ],
        )
    end = events[-1]
    if end["type"] == "end" and end.get("summary") is not None:
        conn.execute(
            "insert into simulation_results(run_id,metrics) values (%s,%s)",
            (rid, Jsonb(end)),
        )
        conn.execute(
            "update simulation_runs set status='completed', completed_at=now() where id=%s",
            (rid,),
        )
    else:
        conn.execute(
            "update simulation_runs set status='failed',error_message='Incomplete imported recording' where id=%s",
            (rid,),
        )


def import_legacy(conn, project, scenario):
    from psycopg.types.json import Jsonb

    if not conn.execute(
        "select id from scenarios where id=%s and project_id=%s and simulation_type='prompt_injection'",
        (scenario, project),
    ).fetchone():
        raise ValueError(
            "Select a prompt-injection scenario belonging to the import project"
        )
    present = conn.execute(
        "select to_regclass('chonkvid_runs') as runs,to_regclass('chonkvid_results') as results"
    ).fetchone()
    if present["runs"]:
        for row in conn.execute("select * from chonkvid_runs"):
            if len(row["body"]) != row["event_count"]:
                raise ValueError("Legacy recording event count mismatch")
            import_run(
                conn, project, scenario, row["run_id"], row["body"], row["created_at"]
            )
    if present["results"]:
        for row in conn.execute("select * from chonkvid_results order by id"):
            conn.execute(
                """insert into simulation_reports(project_id,kind,body,legacy_result_id,created_at)
                values (%s,%s,%s,%s,%s) on conflict(project_id,legacy_result_id) do nothing""",
                (
                    project,
                    row["kind"],
                    Jsonb(row["body"]),
                    row["id"],
                    row["created_at"],
                ),
            )


def init_schema():
    if not check()["ok"]:
        raise RuntimeError("Apply supabase/migrations using the Supabase CLI first")


def sync_run_file(path):
    if enabled():
        with connect() as conn:
            events = [
                json.loads(line)
                for line in path.read_text().splitlines()
                if line.strip()
            ]
            import_run(
                conn,
                os.environ["SUPABASE_PROJECT_ID"],
                os.environ["SUPABASE_SCENARIO_ID"],
                path.name,
                events,
            )


def upsert_latest(kind, body):
    if enabled():
        from psycopg.types.json import Jsonb

        with connect() as conn:
            conn.execute(
                "insert into simulation_reports(project_id,kind,body) values (%s,%s,%s)",
                (os.environ["SUPABASE_PROJECT_ID"], kind, Jsonb(body)),
            )
