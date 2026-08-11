from app.providers.base import BaseProvider

_registry: list[BaseProvider] = []


def register(provider: BaseProvider) -> None:
    _registry.append(provider)


def all_providers() -> list[BaseProvider]:
    return list(_registry)
