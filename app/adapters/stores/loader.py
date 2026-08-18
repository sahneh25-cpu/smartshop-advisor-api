from typing import List

from app.adapters.stores.base_store import BaseStoreAdapter
from app.adapters.stores.active.digikala_adapter import DigikalaAdapter
from app.adapters.stores.active.torob_adapter import TorobAdapter


def get_active_store_adapters() -> List[BaseStoreAdapter]:
    """
    Step-1 loader (explicit imports).
    Later we can upgrade to dynamic discovery via pkgutil/importlib.
    """
    return [
        DigikalaAdapter(),
        TorobAdapter(),
    ]
