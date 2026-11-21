"""Live RLS integration tests against a real (throwaway) Supabase project.

These are NOT run in the default suite: they need a dedicated test project and are
skipped unless all SUPABASE_TEST_* env vars are set:

    SUPABASE_TEST_URL                  e.g. https://xyzcompany.supabase.co
    SUPABASE_TEST_SERVICE_KEY          service_role key (server-side, test project only)
    SUPABASE_TEST_ANON_KEY             anon / publishable key

Run with:
    SUPABASE_TEST_URL=... SUPABASE_TEST_SERVICE_KEY=... SUPABASE_TEST_ANON_KEY=... \
        python -m pytest tests/test_rls_live.py -v

Never point these at a shared or production project: the tests create and delete
auth users, projects and rows.
"""

import os
import uuid

import pytest

pytestmark = pytest.mark.skipif(
    not all(os.environ.get(k) for k in
            ("SUPABASE_TEST_URL", "SUPABASE_TEST_SERVICE_KEY", "SUPABASE_TEST_ANON_KEY")),
    reason="set SUPABASE_TEST_URL / SUPABASE_TEST_SERVICE_KEY / SUPABASE_TEST_ANON_KEY "
           "to run live RLS tests against a throwaway project")

supabase = pytest.importorskip("supabase")

URL = os.environ.get("SUPABASE_TEST_URL", "")
SERVICE = os.environ.get("SUPABASE_TEST_SERVICE_KEY", "")
ANON = os.environ.get("SUPABASE_TEST_ANON_KEY", "")


def _admin():
    return supabase.create_client(URL, SERVICE)


def _user_client(email, password):
    c = supabase.create_client(URL, ANON)
    c.auth.sign_in_with_password({"email": email, "password": password})
    return c


@pytest.fixture
def users():
    admin = _admin()
    identities = []
    clients = []
    try:
        for _ in range(3):
            email = f"rls-{uuid.uuid4().hex}@example.com"
            password = uuid.uuid4().hex + "Aa1!"
            user = admin.auth.admin.create_user({
                "email": email, "password": password, "email_confirm": True,
            }).user
            identities.append(user.id)
            clients.append(_user_client(email, password))
        yield admin, clients, identities
    finally:
        for user_id in identities:
            admin.auth.admin.delete_user(user_id)


def test_rls_project_isolation_and_privilege_escalation(users):
    from postgrest.exceptions import APIError

    admin, (alice, bob, outsider), (alice_id, bob_id, outsider_id) = users
    with pytest.raises(APIError) as foreign_owner:
        alice.table("projects").insert({"name": "invalid", "owner_id": outsider_id}).execute()
    assert foreign_owner.value.code == "42501"

    project = alice.table("projects").insert(
        {"name": "alice project", "owner_id": alice_id}).execute().data[0]
    pid = project["id"]
    members = alice.table("project_members").select("*").eq("project_id", pid).execute().data
    assert [(m["user_id"], m["role"]) for m in members] == [(alice_id, "owner")]
    assert bob.table("projects").select("*").eq("id", pid).execute().data == []
    with pytest.raises(APIError) as self_add:
        bob.table("project_members").insert(
            {"project_id": pid, "user_id": bob_id, "role": "admin"}).execute()
    assert self_add.value.code == "42501"

    alice.table("project_members").insert(
        {"project_id": pid, "user_id": bob_id, "role": "member"}).execute()
    assert bob.table("projects").update({"owner_id": bob_id}).eq("id", pid).execute().data == []
    assert bob.table("project_members").update({"role": "admin"}).eq(
        "project_id", pid).eq("user_id", bob_id).execute().data == []

    alice.table("project_members").update({"role": "admin"}).eq(
        "project_id", pid).eq("user_id", bob_id).execute()
    with pytest.raises(APIError) as owner_update:
        bob.table("projects").update({"owner_id": bob_id}).eq("id", pid).execute()
    assert owner_update.value.code == "23514"
    assert bob.table("project_members").update({"role": "member"}).eq(
        "project_id", pid).eq("user_id", alice_id).execute().data == []
    assert alice.table("projects").select("owner_id").eq("id", pid).execute().data[0]["owner_id"] == alice_id

    second = outsider.table("projects").insert(
        {"name": "outsider project", "owner_id": outsider_id}).execute().data[0]["id"]
    scenario = alice.table("scenarios").insert({
        "project_id": pid, "simulation_type": "prompt_injection", "name": "scenario",
    }).execute().data[0]["id"]

    row = {"scenario_id": scenario, "project_id": second, "mode": "mock"}
    with pytest.raises(APIError) as mismatch:
        admin.table("simulation_runs").insert(row).execute()
    assert mismatch.value.code == "23503"

    rid = alice.table("simulation_runs").insert(
        dict(row, project_id=pid)).execute().data[0]["id"]
    assert not outsider.table("simulation_runs").select("*").eq("id", rid).execute().data
    assert bob.table("simulation_runs").select("*").eq("id", rid).execute().data
    with pytest.raises(APIError) as premature:
        bob.table("simulation_runs").update({"status": "completed"}).eq("id", rid).execute()
    assert premature.value.code == "23514"

    bob.table("simulation_events").insert({
        "run_id": rid, "sequence_number": 0, "event_type": "end", "payload": {"type": "end"},
    }).execute()
    bob.table("simulation_results").insert({
        "run_id": rid, "metrics": {"summary": {"attack_rate": 0.1}},
    }).execute()
    completed = bob.table("simulation_runs").update(
        {"status": "completed"}).eq("id", rid).execute().data[0]
    assert completed["status"] == "completed"
    assert not outsider.table("simulation_events").select("*").eq("run_id", rid).execute().data
    assert not outsider.table("simulation_results").select("*").eq("run_id", rid).execute().data


def test_fastapi_remote_reads_with_live_tokens(users, monkeypatch):
    from fastapi.testclient import TestClient
    from chonkvid import server
    from chonkvid.supabase_store import SupabaseStore

    _, (alice, bob, outsider), (alice_id, bob_id, _) = users
    pid = alice.table("projects").insert(
        {"name": "api test", "owner_id": alice_id}).execute().data[0]["id"]
    alice.table("project_members").insert(
        {"project_id": pid, "user_id": bob_id, "role": "member"}).execute()
    sid = alice.table("scenarios").insert(
        {"project_id": pid, "simulation_type": "prompt_injection", "name": "api test"}
    ).execute().data[0]["id"]
    rid = alice.table("simulation_runs").insert(
        {"project_id": pid, "scenario_id": sid, "mode": "mock"}
    ).execute().data[0]["id"]
    store = SupabaseStore(url=URL, service_role_key=SERVICE, project_id=pid, scenario_id=sid)
    monkeypatch.setattr(server, "get_store", lambda: store)
    client = TestClient(server.app)
    path = f"/api/persistence/runs/{rid}"
    member_header = {"Authorization": f"Bearer {bob.auth.get_session().access_token}"}
    outsider_header = {"Authorization": f"Bearer {outsider.auth.get_session().access_token}"}
    assert client.get(path).status_code == 401
    assert client.get(path, headers=outsider_header).status_code == 404
    response = client.get(path, headers=member_header)
    assert response.status_code == 200
    assert response.json()["run"]["run_id"] == rid
