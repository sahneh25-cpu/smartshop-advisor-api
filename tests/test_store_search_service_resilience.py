from app.services.store_search_service import StoreSearchService


class OkAdapter:
    store_key = "ok-store"

    def search(self, query, filters, limit):
        return [
            {
                "title": "Mock Product",
                "price": 123,
                "url": "https://example.com/p/1",
                "store": self.store_key,
            }
        ]


class FailingAdapter:
    store_key = "bad-store"

    def search(self, query, filters, limit):
        raise RuntimeError("store is down")


def test_search_all_continues_when_one_adapter_fails(monkeypatch):
    from app.adapters.stores import loader as store_loader

    monkeypatch.setattr(
        store_loader,
        "get_active_store_adapters",
        lambda: [OkAdapter(), FailingAdapter()],
    )

    service = StoreSearchService()
    results = service.search_all(query="لپ تاپ", filters={}, limit_per_store=5)

    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["store"] == "ok-store"
