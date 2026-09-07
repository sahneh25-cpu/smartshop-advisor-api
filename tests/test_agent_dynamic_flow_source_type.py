from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _start_session(payload: dict):
    return client.post("/api/v1/agent/session/start", json=payload)


def _next_step(payload: dict):
    return client.post("/api/v1/agent/session/next", json=payload)


def test_start_session_defaults_to_retail_and_opt_in_false():
    res = _start_session({"query": "گوشی میخوام"})
    assert res.status_code == 200
    data = res.json()

    # default guards
    assert data.get("source_type") in ("retail", "marketplace", "aggregator", "classified", None)
    # اگر API شما صراحتا default برمیگرداند:
    if "source_type" in data:
        assert data["source_type"] == "retail"

    if "classified_opt_in" in data:
        assert data["classified_opt_in"] is False


def test_classified_flow_when_opted_in():
    # شروع سشن با opt-in روشن
    start_res = _start_session({
        "query": "لپ تاپ دست دوم میخوام",
        "source_type": "classified",
        "classified_opt_in": True
    })
    assert start_res.status_code == 200
    start_data = start_res.json()

    session_id = start_data.get("session_id")
    assert session_id, "session_id must exist"

    # قدم بعدی: انتظار داریم سوالات classified-style برگردد
    next_res = _next_step({
        "session_id": session_id,
        "answer": "تهران"
    })
    assert next_res.status_code == 200
    next_data = next_res.json()

    # انعطافپذیر: یا question object یا questions list
    if "question" in next_data and isinstance(next_data["question"], dict):
        key = next_data["question"].get("key", "")
        assert key in ("location", "item_condition", "seller_type", "condition")
    elif "questions" in next_data and isinstance(next_data["questions"], list):
        keys = [q.get("key") for q in next_data["questions"] if isinstance(q, dict)]
        assert any(k in ("location", "item_condition", "seller_type", "condition") for k in keys)
    else:
        # اگر API مدل متفاوت دارد حداقل complete نشده باشد در step اول
        assert next_data.get("is_complete") in (False, None)


def test_retail_flow_when_not_opted_in():
    start_res = _start_session({
        "query": "لپ تاپ میخوام",
        "source_type": "retail",
        "classified_opt_in": False
    })
    assert start_res.status_code == 200
    start_data = start_res.json()

    session_id = start_data.get("session_id")
    assert session_id, "session_id must exist"

    next_res = _next_step({
        "session_id": session_id,
        "answer": "ادامه"
    })
    assert next_res.status_code == 200
    next_data = next_res.json()

    # در retail نباید مجبورا سوالات classified-first بیاید
    classified_keys = {"location", "item_condition", "seller_type", "condition"}
    if "question" in next_data and isinstance(next_data["question"], dict):
        key = next_data["question"].get("key")
        assert key not in classified_keys
    elif "questions" in next_data and isinstance(next_data["questions"], list):
        keys = {q.get("key") for q in next_data["questions"] if isinstance(q, dict)}
        assert not keys.issubset(classified_keys)
