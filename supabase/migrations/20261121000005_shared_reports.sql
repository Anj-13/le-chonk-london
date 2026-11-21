alter table public.simulation_runs add column legacy_run_id text;
alter table public.simulation_runs add constraint simulation_runs_legacy_key unique(project_id, legacy_run_id);

create table public.simulation_reports (
  id bigint generated always as identity primary key,
  project_id uuid not null references public.projects(id) on delete cascade,
  kind text not null check (kind in ('experiment','prompt-test')),
  body jsonb not null,
  created_at timestamptz not null default now(),
  legacy_result_id bigint,
  unique(project_id, legacy_result_id)
);
create index simulation_reports_latest on public.simulation_reports(project_id,kind,created_at desc,id desc);
alter table public.simulation_reports enable row level security;
revoke all on public.simulation_reports from anon, authenticated;
grant select on public.simulation_reports to authenticated;
create policy "members read project reports" on public.simulation_reports for select
  to authenticated using (public.is_project_member(project_id,auth.uid()));
