from app.stores.repository import StoreRepository
from app.stores.schemas import StoreCreate, StoreUpdate
from app.stores.seed_data import SEED_STORES


class StoreService:
    def __init__(self, repo: StoreRepository):
        self.repo = repo

    def list_stores(self):
        return self.repo.list_all()

    def get_store(self, store_id: int):
        return self.repo.get_by_id(store_id)

    def create_store(self, payload: StoreCreate):
        return self.repo.create(payload.model_dump())

    def update_store(self, store_id: int, payload: StoreUpdate):
        return self.repo.update(store_id, payload.model_dump(exclude_none=True))

    def delete_store(self, store_id: int):
        return self.repo.delete(store_id)

    def seed_if_empty(self):
        current = self.repo.list_all()
        if current:
            return current
        for item in SEED_STORES:
            self.repo.create(item)
        return self.repo.list_all()


_store_service_singleton = None


def get_store_service():
    global _store_service_singleton
    if _store_service_singleton is None:
        _store_service_singleton = StoreService(StoreRepository())
    return _store_service_singleton
