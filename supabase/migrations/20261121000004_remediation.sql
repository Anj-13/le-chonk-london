-- Preflight legacy rows before changing constraints. Resolve conflicts explicitly.
do $$
begin
  if exists (
    select 1 from public.simulation_runs r
    join public.scenarios s on s.id = r.scenario_id
    where r.project_id <> s.project_id
  ) then
    raise exception 'Existing simulation runs reference scenarios from another project';
  end if;
  if exists (
    select 1 from public.projects p
    where not exists (
      select 1 from public.project_members m
      where m.project_id = p.id and m.user_id = p.owner_id and m.role = 'owner'
    ) or exists (
      select 1 from public.project_members m
      where m.project_id = p.id and m.user_id <> p.owner_id and m.role = 'owner'
    )
  ) then
    raise exception 'Existing project ownership disagrees with owner membership';
  end if;
  if exists (
    select 1 from public.simulation_runs r
    left join lateral (
      select count(*) as total, min(sequence_number) as first, max(sequence_number) as last
      from public.simulation_events where run_id = r.id
    ) events on true
    where r.status = 'completed' and (
      events.total = 0 or events.first <> 0 or events.last <> events.total - 1
      or not exists (
        select 1 from public.simulation_events e
        where e.run_id = r.id and e.sequence_number = events.last and e.event_type = 'end'
      ) or not exists (
        select 1 from public.simulation_results where run_id = r.id
      )
    )
  ) then
    raise exception 'Existing completed runs have missing events or results';
  end if;
end;
$$;

create unique index project_members_one_owner
  on public.project_members (project_id) where role = 'owner';

create function public.protect_project_owner() returns trigger
language plpgsql set search_path = '' as $$
begin
  if new.owner_id is distinct from old.owner_id then
    raise exception 'Project ownership is immutable' using errcode = '23514';
  end if;
  return new;
end;
$$;

create trigger projects_protect_owner
  before update on public.projects
  for each row execute function public.protect_project_owner();

-- INSERT ... RETURNING evaluates the read policy before the owner trigger runs.
drop policy "projects: members read" on public.projects;
create policy "projects: members read" on public.projects
  for select using (owner_id = auth.uid() or public.is_project_member(id, auth.uid()));

alter table public.scenarios
  add constraint scenarios_id_project_key unique (id, project_id);

alter table public.simulation_runs
  drop constraint simulation_runs_scenario_id_fkey,
  add constraint simulation_runs_scenario_project_fkey
    foreign key (scenario_id, project_id)
    references public.scenarios (id, project_id) on delete cascade;

create function public.guard_simulation_run() returns trigger
language plpgsql set search_path = '' as $$
declare
  event_count bigint;
  first_sequence integer;
  last_sequence integer;
begin
  if tg_op = 'UPDATE' then
    if new.id is distinct from old.id
       or new.project_id is distinct from old.project_id
       or new.scenario_id is distinct from old.scenario_id then
      raise exception 'Run identity and scenario are immutable' using errcode = '23514';
    end if;
    if old.status = 'completed' and new.status = 'completed' then
      return new;
    end if;
  end if;
  if new.status = 'completed' then
    select count(*), min(sequence_number), max(sequence_number)
      into event_count, first_sequence, last_sequence
      from public.simulation_events where run_id = new.id;

    if event_count = 0 or first_sequence <> 0 or last_sequence <> event_count - 1
       or not exists (
         select 1 from public.simulation_events
         where run_id = new.id and sequence_number = last_sequence and event_type = 'end'
       ) or not exists (
         select 1 from public.simulation_results where run_id = new.id
       ) then
      raise exception 'Completion requires a contiguous event log and a result'
        using errcode = '23514';
    end if;
  end if;
  return new;
end;
$$;

create trigger simulation_runs_guard
  before insert or update on public.simulation_runs
  for each row execute function public.guard_simulation_run();
