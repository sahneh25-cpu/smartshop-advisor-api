from app.services.store_search_service import StoreSearchService


def test_search_all_returns_aggregated_results():
    service = StoreSearchService()

    results = service.search_all(
        query="لپ تاپ",
        filters={"max_price": 30_000_000},
        limit_per_store=5,
    )

    assert isinstance(results, list)
    assert len(results) >= 2  # چون حداقل دو آداپتر فعال داریم

    # shape check
    item = results[0]
    assert "title" in item
    assert "price" in item
    assert "url" in item
    assert "store" in item


def test_search_all_respects_limit_per_store():
    service = StoreSearchService()

    results = service.search_all(
        query="گوشی",
        filters={},
        limit_per_store=1,
    )

    # با 2 فروشگاه فعال، انتظار داریم حداکثر 2 نتیجه بگیریم
    assert len(results) <= 2
