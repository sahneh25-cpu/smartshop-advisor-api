from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_dynamic_question_flow_known_category_returns_questions():
    response = client.post(
        "/api/v1/ai/dynamic-question-flow",
        json={"user_query": "\u06af\u0648\u0634\u06cc \u0645\u0648\u0628\u0627\u06cc\u0644"},
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["questions"], list)
    assert len(data["questions"]) > 0
