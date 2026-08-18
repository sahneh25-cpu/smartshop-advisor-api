from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseStoreAdapter(ABC):
    """Contract for all store adapters (plugin style)."""

    @property
    @abstractmethod
    def store_key(self) -> str:
        """Unique machine-readable key, e.g. 'digikala'."""
        raise NotImplementedError

    @property
    @abstractmethod
    def store_name_fa(self) -> str:
        """Human-readable Persian name, e.g. 'دیجی‌کالا'."""
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Return normalized product list:
        [
          {
            "title": str,
            "price": int | None,
            "url": str,
            "store": str,
            "availability": str | None,
            "score": float | None,
            "specs": dict
          }
        ]
        """
        raise NotImplementedError
