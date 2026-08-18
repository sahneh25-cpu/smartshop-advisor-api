from typing import Any, Dict, List, Optional
import logging

from app.adapters.stores import loader as store_loader

logger = logging.getLogger(__name__)


class StoreSearchService:
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

        # None always last (for both asc/desc handled in tuple)
        if value is None:
            return (1, 0)

        # Try numeric sort first
        try:
            return (0, float(value))
        except (TypeError, ValueError):
            pass

        # Fallback string sort (case-insensitive)
        return (0, str(value).lower())

    def search_all(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit_per_store: int = 10,
        sort_by: str = "best_value",
        sort_order: str = "desc",
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        for adapter in store_loader.get_active_store_adapters():
            try:
                items = adapter.search(
                    query=query,
                    filters=filters or {},
                    limit=limit_per_store,
                )

                for item in items:
                    item["value_score"] = self._compute_value_score(item)

                results.extend(items)

            except Exception as exc:
                logger.warning(
                    "Store adapter failed",
                    extra={"store": getattr(adapter, "store_key", "unknown")},
                    exc_info=exc,
                )
                continue

        reverse = sort_order.lower() == "desc"

        if sort_by == "best_value":
            results.sort(
                key=lambda x: self._sort_key_generic(x, "value_score"),
                reverse=reverse,
            )
        else:
            # Generic sorter for any clicked column header
            results.sort(
                key=lambda x: self._sort_key_generic(x, sort_by),
                reverse=reverse,
            )

        return results
