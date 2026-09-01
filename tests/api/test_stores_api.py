from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_stores_crud_flow():
    # create
    res = client.post("/api/v1/stores", json={
        "name": "SnapMarket",
        "slug": "snapmarket",
        "website": "https://snapp.market",
        "search_type": "marketplace",
        "is_active": True,
        "priority": 4
    })
    assert res.status_code == 201, res.text
    created = res.json()
    store_id = created["id"]
    assert created["name"] == "SnapMarket"
    assert created["is_active"] is True

    # list
    res = client.get("/api/v1/stores")
    assert res.status_code == 200, res.text
    assert isinstance(res.json(), list)

    # get by id
    res = client.get(f"/api/v1/stores/{store_id}")
    assert res.status_code == 200, res.text
    assert res.json()["id"] == store_id

    # update
    res = client.put(f"/api/v1/stores/{store_id}", json={
        "name": "SnapMarket Updated",
        "is_active": False
    })
    assert res.status_code == 200, res.text
    updated = res.json()
    assert updated["name"] == "SnapMarket Updated"
    assert updated["is_active"] is False

    # delete
    res = client.delete(f"/api/v1/stores/{store_id}")
    assert res.status_code in (200, 204), res.text

    # confirm delete
    res = client.get(f"/api/v1/stores/{store_id}")
    assert res.status_code == 404, res.text
