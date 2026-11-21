-- Covid19-sim: core schema (Phase 1).
--
-- Two simulation models share this schema and are distinguished ONLY by
-- scenarios.simulation_type ('prompt_injection' | 'disease_outbreak'). Metrics and
-- configuration are opaque JSONB: prompt-injection metrics (attack rate, R0, ...) are
-- NOT epidemiological measurements, and no clinical fields are invented here.
--
-- Apply order: 20261121000001_schema.sql -> 20261121000002_rls.sql -> 20261121000003_storage.sql

create extension if not exists pgcrypto;

-- ---------------------------------------------------------------------------
-- updated_at maintenance
-- ---------------------------------------------------------------------------
create or replace function public.set_updated_at() returns trigger
language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- ---------------------------------------------------------------------------
-- profiles: one row per Supabase Auth user
-- ---------------------------------------------------------------------------
create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  display_name text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- projects + membership
-- ---------------------------------------------------------------------------
create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  owner_id uuid not null references auth.users (id) on delete cascade,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.project_members (
  project_id uuid not null references public.projects (id) on delete cascade,
  user_id uuid not null references auth.users (id) on delete cascade,
  -- 'owner' rows are created only by the trigger below (SECURITY DEFINER), never
  -- through the API, so clients cannot grant themselves ownership.
  role text not null check (role in ('owner', 'admin', 'member')),
  created_at timestamptz not null default now(),
  primary key (project_id, user_id)
);

-- Every new project gets an 'owner' membership row for its creator, inserted with
-- elevated privileges so the RLS policies on project_members never need to let a
-- client write role = 'owner'.
create or replace function public.add_owner_membership() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.project_members (project_id, user_id, role)
  values (new.id, new.owner_id, 'owner');
  return new;
end;
$$;

drop trigger if exists projects_add_owner on public.projects;
create trigger projects_add_owner
  after insert on public.projects
  for each row execute function public.add_owner_membership();

-- ---------------------------------------------------------------------------
-- scenarios: named, versioned simulation configurations per project
-- ---------------------------------------------------------------------------
create table if not exists public.scenarios (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects (id) on delete cascade,
  simulation_type text not null check (simulation_type in ('prompt_injection', 'disease_outbreak')),
  name text not null,
  config jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists scenarios_project_type_idx
  on public.scenarios (project_id, simulation_type);

-- ---------------------------------------------------------------------------
-- simulation_runs: one execution of a scenario
-- ---------------------------------------------------------------------------
create table if not exists public.simulation_runs (
  id uuid primary key default gen_random_uuid(),
  scenario_id uuid not null references public.scenarios (id) on delete cascade,
  -- Denormalized so RLS policies can check project membership without a join.
  project_id uuid not null references public.projects (id) on delete cascade,
  status text not null default 'pending'
    check (status in ('pending', 'running', 'completed', 'failed')),
  mode text not null check (mode in ('mock', 'live')),
  model_metadata jsonb not null default '{}'::jsonb,
  -- Snapshot of the scenario config actually used, so a run is replayable even if
  -- the scenario row is later edited.
  config jsonb not null default '{}'::jsonb,
  error_message text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  started_at timestamptz,
  completed_at timestamptz
);

create index if not exists simulation_runs_project_idx
  on public.simulation_runs (project_id, created_at desc);
create index if not exists simulation_runs_scenario_idx
  on public.simulation_runs (scenario_id, created_at desc);
create index if not exists simulation_runs_status_idx
  on public.simulation_runs (status);

-- ---------------------------------------------------------------------------
-- simulation_events: append-only, deterministically replayable event log
-- ---------------------------------------------------------------------------
create table if not exists public.simulation_events (
  id uuid primary key default gen_random_uuid(),
  run_id uuid not null references public.simulation_runs (id) on delete cascade,
  sequence_number integer not null check (sequence_number >= 0),
  -- Simulation tick the event belongs to; NULL for tick-agnostic events (start/end).
  tick integer,
  event_type text not null,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  -- Deterministic replay: one event per (run, sequence).
  unique (run_id, sequence_number)
);

create index if not exists simulation_events_run_seq_idx
  on public.simulation_events (run_id, sequence_number);

-- ---------------------------------------------------------------------------
-- simulation_results: exactly one metrics row per run
-- ---------------------------------------------------------------------------
create table if not exists public.simulation_results (
  run_id uuid primary key references public.simulation_runs (id) on delete cascade,
  metrics jsonb not null default '{}'::jsonb,
  report_path text,
  created_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- report_submissions: citizen-style reports (text or voice) against a project.
-- Voice recordings and health-related content are sensitive even in a demo:
-- synthetic data only, audio lives in a private bucket (see 0003_storage.sql).
-- ---------------------------------------------------------------------------
create table if not exists public.report_submissions (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects (id) on delete cascade,
  created_by uuid not null references auth.users (id) on delete cascade,
  input_type text not null check (input_type in ('text', 'voice')),
  transcript text,
  observations jsonb not null default '{}'::jsonb,
  audio_path text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists report_submissions_project_idx
  on public.report_submissions (project_id, created_at desc);

-- ---------------------------------------------------------------------------
-- updated_at triggers
-- ---------------------------------------------------------------------------
do $$
declare
  t text;
begin
  foreach t in array array['profiles', 'projects', 'scenarios', 'simulation_runs', 'report_submissions'] loop
    execute format('drop trigger if exists set_updated_at on public.%I', t);
  end loop;
end $$;

create trigger set_updated_at before update on public.profiles
  for each row execute function public.set_updated_at();
create trigger set_updated_at before update on public.projects
  for each row execute function public.set_updated_at();
create trigger set_updated_at before update on public.scenarios
  for each row execute function public.set_updated_at();
create trigger set_updated_at before update on public.simulation_runs
  for each row execute function public.set_updated_at();
create trigger set_updated_at before update on public.report_submissions
  for each row execute function public.set_updated_at();
