from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class ProductResult:
    title: str
    url: Optional[str]
    source: str
    region: str
    price: Optional[float] = None
    currency: str = "IRR"
    image_url: Optional[str] = None
    extra: dict = field(default_factory=dict)


class BaseProvider(ABC):
    name: str = ""
    region: str = ""

    @abstractmethod
    async def search(self, query: str, limit: int = 10, budget: Optional[float] = None) -> list[ProductResult]:
        pass
