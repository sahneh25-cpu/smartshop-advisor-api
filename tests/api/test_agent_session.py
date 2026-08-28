from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_start_session():
    res = client.post("/api/v1/agent/session/start", json={"user_query": "گوشی می‌خوام"})
    assert res.status_code == 200
    data = res.json()
    assert data["session_id"]
    assert data["current_question"]
    assert data["is_complete"] is False


def test_next_session():
    start = client.post("/api/v1/agent/session/start", json={"user_query": "گوشی می‌خوام"})
    session_id = start.json()["session_id"]

    res = client.post(
        "/api/v1/agent/session/next",
        json={"session_id": session_id, "user_answer": "تا 20 میلیون"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["session_id"] == session_id
    assert data["current_question"]


def test_next_session_with_invalid_session_id_returns_404():
    res = client.post(
        "/api/v1/agent/session/next",
        json={"session_id": "does-not-exist", "user_answer": "تا 20 میلیون"},
    )
    assert res.status_code == 404
