class StoreRepository:
    def __init__(self):
        self._stores = []
        self._next_id = 1

    def list_all(self):
        return sorted(self._stores, key=lambda x: x.get("priority", 100))

    def get_by_id(self, store_id: int):
        for s in self._stores:
            if s["id"] == store_id:
                return s
        return None

    def create(self, data: dict):
        item = {**data, "id": self._next_id}
        self._next_id += 1
        self._stores.append(item)
        return item

    def update(self, store_id: int, data: dict):
        store = self.get_by_id(store_id)
        if not store:
            return None
        store.update(data)
        return store

    def delete(self, store_id: int):
        store = self.get_by_id(store_id)
        if not store:
            return False
        self._stores = [s for s in self._stores if s["id"] != store_id]
        return True
