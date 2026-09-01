"""Auto-discover store adapters from ``app.adapters.stores.active``.

Adding a shop: create one Python file in that folder that subclasses
``BaseStoreAdapter``. Do not edit this loader or any other core module.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from typing import List

from app.adapters.stores import active as active_pkg
from app.adapters.stores.base_store import BaseStoreAdapter


def get_active_store_adapters() -> List[BaseStoreAdapter]:
    adapters: List[BaseStoreAdapter] = []
    seen_keys = set()

    for info in pkgutil.iter_modules(active_pkg.__path__):
        if info.name.startswith("_"):
            continue
        module = importlib.import_module(f"{active_pkg.__name__}.{info.name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if obj is BaseStoreAdapter or not issubclass(obj, BaseStoreAdapter):
                continue
            if obj.__module__ != module.__name__:
                continue
            instance = obj()
            key = instance.store_key
            if key in seen_keys:
                continue
            seen_keys.add(key)
            adapters.append(instance)

    return adapters
