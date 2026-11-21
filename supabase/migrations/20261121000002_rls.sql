-- Covid19-sim: Row Level Security (Phase 2).
--
-- Model: authenticated users reach only projects they belong to. Membership is
-- checked through SECURITY DEFINER helper functions that run as the function owner,
-- so policies never recurse through the tables they protect.
--
-- Privilege-escalation rules enforced here:
--   * a user can never insert a project_members row for themselves unless they are
--     already an admin of that project (is_project_admin must already be true);
--   * role = 'owner' rows can only be created by the SECURITY DEFINER trigger in
--     0001, and API insert/update policies only accept ('admin', 'member');
--   * the owner membership row itself is immutable and undeletable via the API.
--
-- The backend server uses the service-role key, which bypasses RLS; never ship that
-- key to browsers (see docs/SUPABASE_BACKEND.md).

-- ---------------------------------------------------------------------------
-- enable RLS on every application table
-- ---------------------------------------------------------------------------
alter table public.profiles enable row level security;
alter table public.projects enable row level security;
alter table public.project_members enable row level security;
alter table public.scenarios enable row level security;
alter table public.simulation_runs enable row level security;
alter table public.simulation_events enable row level security;
alter table public.simulation_results enable row level security;
alter table public.report_submissions enable row level security;

-- Explicit grants: RLS still applies to these roles; anon gets nothing.
revoke all on all tables in schema public from anon, authenticated;
grant select, insert, update, delete on public.profiles to authenticated;
grant select, insert, update, delete on public.projects to authenticated;
grant select, insert, update, delete on public.project_members to authenticated;
grant select, insert, update, delete on public.scenarios to authenticated;
grant select, insert, update, delete on public.simulation_runs to authenticated;
grant select, insert on public.simulation_events to authenticated;  -- append-only log
grant select, insert, update on public.simulation_results to authenticated;
grant select, insert, update, delete on public.report_submissions to authenticated;

-- ---------------------------------------------------------------------------
-- membership helpers (SECURITY DEFINER => no recursive RLS)
-- ---------------------------------------------------------------------------
create or replace function public.is_project_member(p_project_id uuid, p_user_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.project_members m
    where m.project_id = p_project_id and m.user_id = p_user_id
  ) or exists (
    select 1 from public.projects p
    where p.id = p_project_id and p.owner_id = p_user_id
  );
$$;

create or replace function public.is_project_admin(p_project_id uuid, p_user_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.project_members m
    where m.project_id = p_project_id and m.user_id = p_user_id
      and m.role in ('owner', 'admin')
  ) or exists (
    select 1 from public.projects p
    where p.id = p_project_id and p.owner_id = p_user_id
  );
$$;

-- True when the user may read/write rows of the given run (via its project).
create or replace function public.can_access_run(p_run_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.simulation_runs r
    where r.id = p_run_id and public.is_project_member(r.project_id, auth.uid())
  );
$$;

-- ---------------------------------------------------------------------------
-- profiles
-- ---------------------------------------------------------------------------
drop policy if exists "profiles: self or co-member read" on public.profiles;
create policy "profiles: self or co-member read" on public.profiles
  for select using (
    auth.uid() = id
    or exists (
      select 1
      from public.project_members a
      join public.project_members b on b.project_id = a.project_id
      where a.user_id = auth.uid() and b.user_id = profiles.id
    )
  );

drop policy if exists "profiles: self insert" on public.profiles;
create policy "profiles: self insert" on public.profiles
  for insert with check (auth.uid() = id);

drop policy if exists "profiles: self update" on public.profiles;
create policy "profiles: self update" on public.profiles
  for update using (auth.uid() = id) with check (auth.uid() = id);

-- ---------------------------------------------------------------------------
-- projects
-- ---------------------------------------------------------------------------
drop policy if exists "projects: members read" on public.projects;
create policy "projects: members read" on public.projects
  for select using (public.is_project_member(id, auth.uid()));

drop policy if exists "projects: owner creates" on public.projects;
create policy "projects: owner creates" on public.projects
  for insert with check (auth.uid() = owner_id);

drop policy if exists "projects: admins update" on public.projects;
create policy "projects: admins update" on public.projects
  for update using (public.is_project_admin(id, auth.uid()));

drop policy if exists "projects: owner deletes" on public.projects;
create policy "projects: owner deletes" on public.projects
  for delete using (auth.uid() = owner_id);

-- ---------------------------------------------------------------------------
-- project_members: read for members; manage only for admins; never self-add,
-- never role='owner' via API, never touch the owner row.
-- ---------------------------------------------------------------------------
drop policy if exists "members: members read" on public.project_members;
create policy "members: members read" on public.project_members
  for select using (public.is_project_member(project_id, auth.uid()));

drop policy if exists "members: admins add non-owner roles" on public.project_members;
create policy "members: admins add non-owner roles" on public.project_members
  for insert with check (
    public.is_project_admin(project_id, auth.uid())
    and role in ('admin', 'member')
  );

drop policy if exists "members: admins update non-owner rows" on public.project_members;
create policy "members: admins update non-owner rows" on public.project_members
  for update
  using (public.is_project_admin(project_id, auth.uid()) and role <> 'owner')
  with check (public.is_project_admin(project_id, auth.uid()) and role in ('admin', 'member'));

drop policy if exists "members: admins remove non-owner rows" on public.project_members;
create policy "members: admins remove non-owner rows" on public.project_members
  for delete using (public.is_project_admin(project_id, auth.uid()) and role <> 'owner');

-- ---------------------------------------------------------------------------
-- scenarios
-- ---------------------------------------------------------------------------
drop policy if exists "scenarios: members read" on public.scenarios;
create policy "scenarios: members read" on public.scenarios
  for select using (public.is_project_member(project_id, auth.uid()));

drop policy if exists "scenarios: members create" on public.scenarios;
create policy "scenarios: members create" on public.scenarios
  for insert with check (public.is_project_member(project_id, auth.uid()));

drop policy if exists "scenarios: admins update" on public.scenarios;
create policy "scenarios: admins update" on public.scenarios
  for update using (public.is_project_admin(project_id, auth.uid()));

drop policy if exists "scenarios: admins delete" on public.scenarios;
create policy "scenarios: admins delete" on public.scenarios
  for delete using (public.is_project_admin(project_id, auth.uid()));

-- ---------------------------------------------------------------------------
-- simulation_runs
-- ---------------------------------------------------------------------------
drop policy if exists "runs: members read" on public.simulation_runs;
create policy "runs: members read" on public.simulation_runs
  for select using (public.is_project_member(project_id, auth.uid()));

drop policy if exists "runs: members create" on public.simulation_runs;
create policy "runs: members create" on public.simulation_runs
  for insert with check (public.is_project_member(project_id, auth.uid()));

drop policy if exists "runs: members update status" on public.simulation_runs;
create policy "runs: members update status" on public.simulation_runs
  for update using (public.is_project_member(project_id, auth.uid()));

drop policy if exists "runs: admins delete" on public.simulation_runs;
create policy "runs: admins delete" on public.simulation_runs
  for delete using (public.is_project_admin(project_id, auth.uid()));

-- ---------------------------------------------------------------------------
-- simulation_events: append-only, readable by project members
-- ---------------------------------------------------------------------------
drop policy if exists "events: members read" on public.simulation_events;
create policy "events: members read" on public.simulation_events
  for select using (public.can_access_run(run_id));

drop policy if exists "events: members append" on public.simulation_events;
create policy "events: members append" on public.simulation_events
  for insert with check (public.can_access_run(run_id));

-- no update/delete policy: the event log is immutable (removed only by cascade
-- when an admin deletes the run).

-- ---------------------------------------------------------------------------
-- simulation_results: one row per run, members read, members upsert
-- ---------------------------------------------------------------------------
drop policy if exists "results: members read" on public.simulation_results;
create policy "results: members read" on public.simulation_results
  for select using (public.can_access_run(run_id));

drop policy if exists "results: members upsert" on public.simulation_results;
create policy "results: members upsert" on public.simulation_results
  for insert with check (public.can_access_run(run_id));

drop policy if exists "results: members update" on public.simulation_results;
create policy "results: members update" on public.simulation_results
  for update using (public.can_access_run(run_id));

-- ---------------------------------------------------------------------------
-- report_submissions: members read/create; creator or admin update/delete
-- ---------------------------------------------------------------------------
drop policy if exists "reports: members read" on public.report_submissions;
create policy "reports: members read" on public.report_submissions
  for select using (public.is_project_member(project_id, auth.uid()));

drop policy if exists "reports: members create own" on public.report_submissions;
create policy "reports: members create own" on public.report_submissions
  for insert with check (
    public.is_project_member(project_id, auth.uid()) and auth.uid() = created_by
  );

drop policy if exists "reports: creator or admin update" on public.report_submissions;
create policy "reports: creator or admin update" on public.report_submissions
  for update using (
    auth.uid() = created_by or public.is_project_admin(project_id, auth.uid())
  );

drop policy if exists "reports: creator or admin delete" on public.report_submissions;
create policy "reports: creator or admin delete" on public.report_submissions
  for delete using (
    auth.uid() = created_by or public.is_project_admin(project_id, auth.uid())
  );
