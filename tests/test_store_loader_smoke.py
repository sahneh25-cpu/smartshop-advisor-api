from app.adapters.stores.loader import get_active_store_adapters


def test_store_loader_returns_adapters():
    adapters = get_active_store_adapters()
    assert len(adapters) >= 2

    keys = {a.store_key for a in adapters}
    assert "digikala" in keys
    assert "torob" in keys


def test_digikala_adapter_search_shape():
    adapters = {a.store_key: a for a in get_active_store_adapters()}
    adapter = adapters["digikala"]

    results = adapter.search(query="لپ تاپ", filters={"max_price": 30_000_000}, limit=10)
    assert isinstance(results, list)

    if results:
        item = results[0]
        assert "title" in item
        assert "price" in item
        assert "url" in item
        assert "store" in item


def test_torob_adapter_search_shape():
    adapters = {a.store_key: a for a in get_active_store_adapters()}
    adapter = adapters["torob"]

    results = adapter.search(query="لپ تاپ", filters={"max_price": 30_000_000}, limit=10)
    assert isinstance(results, list)

    if results:
        item = results[0]
        assert "title" in item
        assert "price" in item
        assert "url" in item
        assert "store" in item
