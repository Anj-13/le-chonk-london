# Covid19-sim — Supabase Backend

Secure, optional Supabase persistence for the ChonkVid/Covid19-sim backend, on branch
`feat/supabase-backend`. Everything here is **additive**: with no Supabase env vars
configured the app runs exactly as before (local JSONL recordings + local results).

## What was found in the repo (Phase 0)

- Backend: `chonkvid/chonkvid/server.py` (FastAPI) + `sim.py` (`run_epidemic` async
  event stream) + `experiment.py` (`Recorder` writes `runs/<stamp>-<label>.jsonl`).
- Event schema produced by `run_epidemic` (all dicts with a `type` field):

  | `type` | key fields |
  |---|---|
  | `start` | `config`, `world`, `vaccinated`, `patient_zero`, `source` |
  | `infection` | `tick`, `agent`, `parent`, `vaccinated?`, `message`, `verdict` |
  | `exposure` | `tick`, `from`, `to`, `channel` |
  | `tick` | `tick`, `phase` (`exposed`/`resolved`), `counts{S,E,I,R}`, `states` |
  | `resisted` | `tick`, `agent`, `parent`, `vaccinated?`, `message`, `verdict` |
  | `recovered` | `tick`, `agent` |
  | `sitrep` | `tick`, `text` (WHO/Mistral-agent report) |
  | `end` | `summary`, `usage`, `source` |

  The server adds `recorded {id}` and `error {message}` on the WebSocket.
- Local recording/replay: `Recorder` JSONL under `CHONKVID_RUNS_DIR` (default
  `chonkvid/runs/`), replayed via `GET /api/runs` and `GET /api/runs/{run_id}`.
- Before this branch there were no Supabase files, migrations, or branches.

## Layout

```
supabase/migrations/20261121000001_schema.sql     tables, constraints, indexes, triggers
supabase/migrations/20261121000002_rls.sql        RLS policies + SECURITY DEFINER helpers
supabase/migrations/20261121000003_storage.sql    private buckets + storage policies
supabase/migrations/20261121000004_remediation.sql ownership, composite foreign key and completion guard
chonkvid/chonkvid/persistence.py                  store protocol, LocalStore, get_store()
chonkvid/chonkvid/supabase_store.py               SupabaseStore (official SDK, async-safe)
chonkvid/chonkvid/server.py                       optional mirror in /ws/run + new read endpoints
chonkvid/tests/test_supabase_backend.py           unit/integration tests (run offline)
chonkvid/tests/test_rls_live.py                   live RLS tests (need a throwaway project)
docs/SUPABASE_BACKEND.md                          this file
```

## Setup

1. Create a Supabase project (or `supabase init` + `supabase start` for local dev).
2. Apply the migrations **in order** (SQL editor or `supabase db push`):
   `00001_schema`, `00002_rls`, `00003_storage`, then `00004_remediation`.
   Apply to a disposable or development project first. The fourth migration refuses
   existing cross-project run references, inconsistent ownership, and incomplete rows
   labeled completed. Inspect and explicitly resolve any conflicts before retrying.
   The migration preserves existing rows.
3. In the project's API settings, copy the URL, the **anon/publishable** key and the
   **service-role** key.
4. `cd chonkvid && python -m venv .venv && .venv/Scripts/pip install -r requirements.txt`
   (on Linux/macOS use `.venv/bin/pip`).
5. Copy `.env.example` to `.env` and fill in:

   | Variable | Where | Notes |
   |---|---|---|
   | `PERSISTENCE_BACKEND` | server | `local` (default) or `supabase` |
   | `SUPABASE_URL` | server | `https://<project>.supabase.co` |
   | `SUPABASE_ANON_KEY` | browser-safe | publishable/anon key; RLS applies |
   | `SUPABASE_SERVICE_ROLE_KEY` | **server only** | bypasses RLS; never commit or ship |
   | `SIMULATION_TYPE` | server | `prompt_injection` (default) or `disease_outbreak` |
   | `SUPABASE_PROJECT_ID` / `SUPABASE_SCENARIO_ID` | server, recommended | select an existing project/scenario pair |
   | `SUPABASE_PROJECT_NAME`, `SUPABASE_SERVICE_EMAIL`, `SUPABASE_SERVICE_PASSWORD` | server, optional | bootstrap of the default project/scenario |

6. Run `python -m chonkvid serve` and check `GET /api/persistence`.
   Grant dashboard users membership in the configured project. Use an access token
   from a signed-in Supabase user in that same project. The publishable/anon key
   is used to sign in via Supabase Auth.

## Baseline schema inventory

This inventory describes migrations 00001 through 00003. All eight tables exist.
Migration 00004 adds constraints and triggers without changing the column inventory.
Simulation type is stored on scenarios. Configuration and metrics remain opaque JSONB.

| Table | Actual columns | Primary key | Foreign keys | RLS policies | Missing constraints |
|---|---|---|---|---|---|
| `profiles` | `id`, `display_name`, `created_at`, `updated_at` | `id` | `id` to `auth.users` | Self or co-member read, self create and update | None required |
| `projects` | `id`, `name`, `owner_id`, `created_at`, `updated_at` | `id` | `owner_id` to `auth.users` | Member read, owner create and delete, admin update | Immutable `owner_id` |
| `project_members` | `project_id`, `user_id`, `role`, `created_at` | `(project_id, user_id)` | `project_id` to `projects`, `user_id` to `auth.users` | Member read, admin management of non-owner roles, owner row created by trigger | One owner row per project |
| `scenarios` | `id`, `project_id`, `simulation_type`, `name`, `config`, `created_at`, `updated_at` | `id` | `project_id` to `projects` | Member read and create, admin update and delete | Composite unique key for the run reference |
| `simulation_runs` | `id`, `scenario_id`, `project_id`, `status`, `mode`, `model_metadata`, `config`, `error_message`, `created_at`, `updated_at`, `started_at`, `completed_at` | `id` | `scenario_id` to `scenarios`, `project_id` to `projects` | Member read, create and update, admin delete | Composite scenario/project FK and completion guard |
| `simulation_events` | `id`, `run_id`, `sequence_number`, `tick`, `event_type`, `payload`, `created_at` | `id` | `run_id` to `simulation_runs` | Member read and append | Existing key covers duplicate sequences. Completeness was unchecked. |
| `simulation_results` | `run_id`, `metrics`, `report_path`, `created_at` | `run_id` | `run_id` to `simulation_runs` | Member read, create and update | No check for a result before run completion |
| `report_submissions` | `id`, `project_id`, `created_by`, `input_type`, `transcript`, `observations`, `audio_path`, `created_at`, `updated_at` | `id` | `project_id` to `projects`, `created_by` to `auth.users` | Member read, member create as self, creator or admin update and delete | No input-type-specific content constraint in the supplied contract |

## Security model

- RLS is enabled on **every** application table; `anon` gets no grants,
  `authenticated` gets table grants but every policy is membership-scoped.
- Membership is checked via `SECURITY DEFINER` helpers `is_project_member`,
  `is_project_admin`, `can_access_run` (`search_path` pinned) — policies never recurse.
- Privilege escalation is blocked: API inserts/updates of `project_members` accept only
  `role ∈ ('admin','member')` and require the caller to already be an admin; the
  `owner` row is created only by a `SECURITY DEFINER` trigger on project insert and is
  immutable/undeletable through the API. Users therefore cannot add themselves to a
  project or change their own role.
- `simulation_events` is append-only (insert policy, no update/delete; cascade on run delete).
- Storage: private buckets `simulation-reports` and `voice-recordings`; object names must
  be `<project_id>/<run_or_submission_id>/<file>` and access is scoped by project
  membership (admins may delete). Voice recordings and health-style reports are treated
  as sensitive: **synthetic data only**, even in a demo.
- The service-role key bypasses RLS and stays server-side. FastAPI verifies access
  tokens with Supabase Auth and derives the project scope from stored membership rows.
- The ownership trigger makes `projects.owner_id` immutable. A partial unique index
  limits owner membership to one row per project. Run identity and scenario are also
  immutable, and a composite foreign key checks the scenario belongs to the run's project.

## Python adapter

`persistence.PersistenceStore` (async protocol), implemented by:

- `LocalStore` — default; JSONL recordings + per-run `*.meta.json` sidecars (the replay
  endpoints only glob `*.jsonl`, so the contract is unchanged). Run id = recording filename.
- `SupabaseStore` — official `supabase` SDK, lazily imported; every blocking call runs in
  `asyncio.to_thread` so the WebSocket loop is never blocked. Events are batch-inserted
  (chunks of up to 500). Replaying an identical `(run_id, sequence_number)` is
  idempotent. Conflicting content at the same sequence raises `PersistenceError`.

Methods: `create_run(mode, simulation_type, label, config, model_metadata, scenario_id)` →
run id; `mark_run_running`, `append_events(run_id, [(seq, event), ...])`,
`complete_run`, `fail_run(run_id, error_message)`, `get_run`, `list_runs(limit)`,
`get_run_events(run_id)` (ordered by `sequence_number`), `save_result(run_id, metrics,
report_path)`. All inputs are validated and raise `PersistenceError` with a clear message.
`get_store()` reads `PERSISTENCE_BACKEND` (cached; `reset_store()` for tests).

## API and replay

`GET /api/persistence` returns only backend configuration status. A configured value
means the adapter could be initialized.

Remote routes require `Authorization: Bearer <Supabase access token>`:

- `GET /api/persistence/runs?limit=60` lists runs in the authenticated user's projects.
- `GET /api/persistence/runs/{run_id}` returns authorized run metadata and ordered
  events, including final metrics in the terminal event for a successful run.
  Inaccessible and nonexistent runs both return 404.
- Absent or invalid tokens return 401. A disabled backend or upstream outage returns 503.

```bash
curl -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}"   http://127.0.0.1:8000/api/persistence/runs
```

The existing dashboard and anonymous WebSocket clients can keep running and replaying
local demo simulations. To opt in to mirroring, an API client supplies a Bearer
header on `/ws/run` or an `access_token` field in the first WebSocket JSON message.
With a configured project, the authenticated user must be a member. For default
bootstrap, provision a confirmed Auth account with `SUPABASE_SERVICE_EMAIL` and use
that account's access token for the server process's first mirror. Configure both
IDs for routine use by other members. Client payloads cannot select the target project.

Authenticated remote attempts record JSONL under `CHONKVID_RUNS_DIR/private/`. Public
demo replay serves only files in the top-level directory. An operator can recover the
private recording by its local filename. Review previously recorded files before
publishing the demo directory because earlier versions stored mirrors alongside
public recordings.

## Persistence failures

The WebSocket `recorded` message keeps the local filename in `id`. It includes
`remote_run_id` only after all ordered event batches and metrics are saved and the
remote status is completed. A failed event batch is retried once using the same
sequence numbers. On persistent failure, local recording continues and
`persistence_error` reports which step failed. The server attempts to mark the remote
row failed. If Supabase also rejects that update, a pending or running row can remain
for operator review. Retained JSONL files are the recovery source.

## Testing

```
cd chonkvid && .venv/Scripts/python.exe -m pytest -q          # 41 passed, 1 skipped
```

Covered offline: migration validity (parsed with the real PostgreSQL grammar via
`pglast`, plus content assertions for tables/RLS/unique constraints/storage policies),
authenticated-access policy structure, run creation and status transitions, ordered
insertion and replay, duplicate `(run_id, sequence_number)` handling, result persistence,
backend failure handling in the WebSocket path (run still completes locally and the
failure is reported), and local-mode backward compatibility (the original suite passes
unchanged).

Live RLS tests (`tests/test_rls_live.py`) verify real cross-project isolation and
privilege-escalation attempts against an actual project. They are **skipped by default**
and were *not* executed in this environment (no live project was provisioned); run them
with:

```
SUPABASE_TEST_URL=... SUPABASE_TEST_SERVICE_KEY=... SUPABASE_TEST_ANON_KEY=... \
  .venv/Scripts/python.exe -m pytest tests/test_rls_live.py -v
```

against a **throwaway** project only. Likewise, no live Mistral/Voxtral behavior was
exercised here — all tests run in mock mode.

## Deployment scope

- The packaged browser UI uses local demo mode. Remote clients handle Supabase sign-in
  and submit access tokens over HTTPS or WSS.
- Runtime bootstrap is a demo convenience. The adapter reuses the SDK's existing
  Auth user and uses deterministic IDs for concurrent default project/scenario creation.
- The local replay and prompt-test APIs are demo features. Limit network access on
  hosts where local demo inputs and outputs require privacy.
- The simulation engine, report upload workflows, and live model behavior are outside
  this persistence change.
