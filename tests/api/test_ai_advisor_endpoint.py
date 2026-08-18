import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.ai import get_advisor_service
from app.schemas.ai import AdvisorInput, AdvisorResponse, Product


client = TestClient(app)


class FakeAdvisorService:
    async def recommend(self, advisor_input: AdvisorInput) -> AdvisorResponse:
        if advisor_input.search_results:
            recommended_product = Product(**advisor_input.search_results[0])
            alternatives = [
                Product(**product_data)
                for product_data in advisor_input.search_results[1:]
            ]

            return AdvisorResponse(
                recommended_product=recommended_product,
                alternatives=alternatives,
                reasoning="Based on the provided search results.",
            )

        if "وجود نداره" in advisor_input.user_query:
            return AdvisorResponse(
                recommended_product=None,
                alternatives=[],
                reasoning="No suitable recommendations found for your query.",
            )

        auto_search_results = [
            {
                "id": 201,
                "name": "Auto Product Alpha",
                "price": 1000.0,
            },
            {
                "id": 202,
                "name": "Auto Product Beta",
                "price": 1200.0,
            },
        ]

        recommended_product = Product(**auto_search_results[0])
        alternatives = [
            Product(**product_data)
            for product_data in auto_search_results[1:]
        ]

        return AdvisorResponse(
            recommended_product=recommended_product,
            alternatives=alternatives,
            reasoning="Based on automated search for your query.",
        )


@pytest.fixture
def override_advisor_service():
    app.dependency_overrides[get_advisor_service] = (
        lambda: FakeAdvisorService()
    )

    yield

    app.dependency_overrides.clear()


def test_advisor_recommend_endpoint_success(override_advisor_service):
    payload = {
        "user_query": "لپ تاپ سبک برای برنامه نویسی می‌خوام",
        "user_answers": {
            "battery": "high",
            "weight": "light",
        },
        "search_results": [
            {
                "id": 1,
                "name": "Laptop A",
                "price": 50000000,
            },
            {
                "id": 2,
                "name": "Laptop B",
                "price": 60000000,
            },
            {
                "id": 3,
                "name": "Laptop C",
                "price": 55000000,
            },
            {
                "id": 4,
                "name": "Laptop D",
                "price": 65000000,
            },
        ],
    }

    response = client.post(
        "/api/v1/ai/advisor/recommend",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recommended_product"] is not None
    assert data["recommended_product"]["id"] == 1
    assert data["recommended_product"]["name"] == "Laptop A"

    assert len(data["alternatives"]) == 3
    assert [product["id"] for product in data["alternatives"]] == [
        2,
        3,
        4,
    ]

    assert isinstance(data["reasoning"], str)
    assert len(data["reasoning"]) > 0


def test_advisor_recommend_endpoint_empty_results(override_advisor_service):
    payload = {
        "user_query": "گوشی اقتصادی که وجود نداره",
        "user_answers": {
            "budget": "very_low",
        },
        "search_results": [],
    }

    response = client.post(
        "/api/v1/ai/advisor/recommend",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recommended_product"] is None
    assert data["alternatives"] == []

    assert isinstance(data["reasoning"], str)
    assert len(data["reasoning"]) > 0


def test_advisor_recommend_endpoint_auto_search(override_advisor_service):
    payload = {
        "user_query": "لپ تاپ خوب برای دانشجو",
        "user_answers": {
            "budget": "medium",
        },
        "search_results": [],
    }

    response = client.post(
        "/api/v1/ai/advisor/recommend",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recommended_product"] is not None
    assert data["recommended_product"]["id"] == 201
    assert data["recommended_product"]["name"] == "Auto Product Alpha"

    assert len(data["alternatives"]) == 1
    assert data["alternatives"][0]["id"] == 202

    assert isinstance(data["reasoning"], str)
    assert len(data["reasoning"]) > 0
