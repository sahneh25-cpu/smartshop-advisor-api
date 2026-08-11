from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_generate_tv_questions():
    response = client.post(
        "/api/v1/ai/product-questions",
        json={"product_name": "تلویزیون"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_type"] == "تلویزیون"
    assert isinstance(data["questions"], list)
    assert len(data["questions"]) >= 3
