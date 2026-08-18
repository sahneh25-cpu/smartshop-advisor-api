from app.services.store_search_service import StoreSearchService


class MockAdapter:
    store_key = "mock"

    def search(self, query, filters, limit):
        return [
            {
                "title": "A",
                "price": 300,
                "spec_score": 90,
                "rating": 4.1,
                "store": "mock",
                "url": "u1",
            },
            {
                "title": "B",
                "price": 100,
                "spec_score": 70,
                "rating": 4.8,
                "store": "mock",
                "url": "u2",
            },
            {
                "title": "C",
                "price": 200,
                "spec_score": 80,
                "rating": 4.5,
                "store": "mock",
                "url": "u3",
            },
        ]


def test_dynamic_sort_by_price_desc(monkeypatch):
    from app.adapters.stores import loader as store_loader
    monkeypatch.setattr(store_loader, "get_active_store_adapters", lambda: [MockAdapter()])

    service = StoreSearchService()
    results = service.search_all(
        query="phone",
        filters={},
        limit_per_store=10,
        sort_by="price",
        sort_order="desc",
    )

    assert [r["price"] for r in results] == [300, 200, 100]


def test_dynamic_sort_by_rating_desc(monkeypatch):
    from app.adapters.stores import loader as store_loader
    monkeypatch.setattr(store_loader, "get_active_store_adapters", lambda: [MockAdapter()])

    service = StoreSearchService()
    results = service.search_all(
        query="phone",
        filters={},
        limit_per_store=10,
        sort_by="rating",
        sort_order="desc",
    )

    assert [r["rating"] for r in results] == [4.8, 4.5, 4.1]


def test_dynamic_sort_by_spec_score_desc(monkeypatch):
    from app.adapters.stores import loader as store_loader
    monkeypatch.setattr(store_loader, "get_active_store_adapters", lambda: [MockAdapter()])

    service = StoreSearchService()
    results = service.search_all(
        query="phone",
        filters={},
        limit_per_store=10,
        sort_by="spec_score",
        sort_order="desc",
    )

    assert [r["spec_score"] for r in results] == [90, 80, 70]
