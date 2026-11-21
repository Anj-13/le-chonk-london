-- Covid19-sim: private storage buckets (Phase 2).
--
-- Buckets hold agent-generated simulation reports and voice report recordings.
-- Both are private (public = false) and sensitive even in a demo — synthetic data
-- only. Object names MUST follow '<project_id>/<run_or_submission_id>/<filename>' so
-- policies can scope access to project members without recursion.

insert into storage.buckets (id, name, public)
values ('simulation-reports', 'simulation-reports', false)
on conflict (id) do nothing;

insert into storage.buckets (id, name, public)
values ('voice-recordings', 'voice-recordings', false)
on conflict (id) do nothing;

revoke all on storage.objects from anon, authenticated;
grant select, insert, delete on storage.objects to authenticated;

-- Extract the project id from an object name, NULL when the name does not start
-- with a UUID (guards the ::uuid cast inside RLS policies).
create or replace function public.object_project_id(p_name text)
returns uuid
language sql
immutable
as $$
  select case
    when (string_to_array(p_name, '/'))[1] ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
      then (string_to_array(p_name, '/'))[1]::uuid
    else null
  end;
$$;

-- ---------------------------------------------------------------------------
-- simulation-reports bucket
-- ---------------------------------------------------------------------------
drop policy if exists "reports bucket: members read" on storage.objects;
create policy "reports bucket: members read" on storage.objects
  for select using (
    bucket_id = 'simulation-reports'
    and public.is_project_member(public.object_project_id(name), auth.uid())
  );

drop policy if exists "reports bucket: members upload" on storage.objects;
create policy "reports bucket: members upload" on storage.objects
  for insert with check (
    bucket_id = 'simulation-reports'
    and public.is_project_member(public.object_project_id(name), auth.uid())
  );

drop policy if exists "reports bucket: admins delete" on storage.objects;
create policy "reports bucket: admins delete" on storage.objects
  for delete using (
    bucket_id = 'simulation-reports'
    and public.is_project_admin(public.object_project_id(name), auth.uid())
  );

-- ---------------------------------------------------------------------------
-- voice-recordings bucket (sensitive: voice reports)
-- ---------------------------------------------------------------------------
drop policy if exists "voice bucket: members read" on storage.objects;
create policy "voice bucket: members read" on storage.objects
  for select using (
    bucket_id = 'voice-recordings'
    and public.is_project_member(public.object_project_id(name), auth.uid())
  );

drop policy if exists "voice bucket: members upload" on storage.objects;
create policy "voice bucket: members upload" on storage.objects
  for insert with check (
    bucket_id = 'voice-recordings'
    and public.is_project_member(public.object_project_id(name), auth.uid())
  );

drop policy if exists "voice bucket: admins delete" on storage.objects;
create policy "voice bucket: admins delete" on storage.objects
  for delete using (
    bucket_id = 'voice-recordings'
    and public.is_project_admin(public.object_project_id(name), auth.uid())
  );
