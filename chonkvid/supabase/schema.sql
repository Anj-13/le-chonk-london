-- ChonkVid tables for Supabase Postgres (project ref ywglfnnbjefqirjjtbhb).
-- Applied automatically by: python -m chonkvid db-init

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

-- Optional: enable RLS if you expose this project via the Data API later.
-- ALTER TABLE chonkvid_results ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE chonkvid_runs ENABLE ROW LEVEL SECURITY;