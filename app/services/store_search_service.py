from typing import Any, Dict, List, Optional
import logging

from app.adapters.stores import loader as store_loader
from app.services.web_source_service import WebSourceService

logger = logging.getLogger(__name__)


class StoreSearchService:
    def __init__(self, web_source: Optional[WebSourceService] = None) -> None:
        self.web_source = web_source or WebSourceService()

    def _compute_value_score(self, item: Dict[str, Any]) -> float:
        spec_score = item.get("spec_score")
        price = item.get("price")
        try:
            spec = float(spec_score)
            pr = float(price)
            if pr <= 0:
                return 0.0
            return spec / pr
        except (TypeError, ValueError):
            return 0.0

    def _sort_key_generic(self, item: Dict[str, Any], field: str) -> Any:
        value = item.get(field, None)

        if value is None:
            return (1, 0)

        try:
            return (0, float(value))
        except (TypeError, ValueError):
            pass

        return (0, str(value).lower())

    def search_all(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit_per_store: int = 10,
        sort_by: str = "best_value",
        sort_order: str = "desc",
        country: Optional[str] = None,
        allow_web_fallback: bool = True,
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        filters = filters or {}

        for adapter in store_loader.get_active_store_adapters():
            try:
                items = adapter.search(
                    query=query,
                    filters=filters,
                    limit=limit_per_store,
                )

                for item in items:
                    item["value_score"] = self._compute_value_score(item)
                    item.setdefault("is_live", True)

                results.extend(items)

            except Exception as exc:
                logger.warning(
                    "Store adapter failed",
                    extra={"store": getattr(adapter, "store_key", "unknown")},
                    exc_info=exc,
                )
                continue

        if not results and allow_web_fallback:
            try:
                web_items = self.web_source.search(
                    query=query,
                    country=country or filters.get("country"),
                    limit=limit_per_store,
                )
                for item in web_items:
                    item["value_score"] = self._compute_value_score(item)
                results.extend(web_items)
            except Exception as exc:
                logger.warning("Web fallback failed: %s", exc)

        reverse = sort_order.lower() == "desc"

        if sort_by == "best_value":
            results.sort(
                key=lambda x: self._sort_key_generic(x, "value_score"),
                reverse=reverse,
            )
        else:
            results.sort(
                key=lambda x: self._sort_key_generic(x, sort_by),
                reverse=reverse,
            )

        return results
