from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_sessions_and_jobs():
    r = client.post("/sessions", json={"session_id": "acc_01", "metadata": {"role": "leader"}})
    assert r.status_code == 200

    r = client.post("/sessions", json={"session_id": "acc_02", "metadata": {"role": "follower"}})
    assert r.status_code == 200

    r = client.post("/mode", json={"mode": "group"})
    assert r.status_code == 200
    assert r.json()["mode"] == "group"

    r = client.post("/jobs", json={"target": "acc_01", "action": "navigate", "payload": {"to": "map_12"}})
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "done"
    assert data["result"]["broadcast_count"] == 2
