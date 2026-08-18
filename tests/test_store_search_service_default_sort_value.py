from app.services.store_search_service import StoreSearchService


class MockAdapter:
    store_key = "mock"

    def search(self, query, filters, limit):
        return [
            {
                "title": "Brand A",
                "price": 300,
                "spec_score": 90,   # value = 0.30
                "url": "u1",
                "store": "mock",
            },
            {
                "title": "Brand B",
                "price": 200,
                "spec_score": 70,   # value = 0.35  -> باید اول باشد
                "url": "u2",
                "store": "mock",
            },
            {
                "title": "Brand C",
                "price": 400,
                "spec_score": 120,  # value = 0.30
                "url": "u3",
                "store": "mock",
            },
        ]


def test_default_sort_is_best_value_desc(monkeypatch):
    from app.adapters.stores import loader as store_loader
    monkeypatch.setattr(store_loader, "get_active_store_adapters", lambda: [MockAdapter()])

    service = StoreSearchService()
    results = service.search_all(query="phone", filters={}, limit_per_store=10)

    assert results[0]["title"] == "Brand B"
