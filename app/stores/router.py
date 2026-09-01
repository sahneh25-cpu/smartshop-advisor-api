from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from .schemas import StoreCreate, StoreUpdate, StoreOut
from .service import StoreService, get_store_service

router = APIRouter()


@router.get("", response_model=list[StoreOut])
def list_stores(
    active: Optional[bool] = Query(default=None),
    service: StoreService = Depends(get_store_service),
):
    items = service.list_stores()
    if active is not None:
        items = [x for x in items if x.get("is_active") == active]
    return items


@router.get("/{store_id}", response_model=StoreOut)
def get_store(store_id: int, service: StoreService = Depends(get_store_service)):
    store = service.get_store(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.post("", response_model=StoreOut, status_code=201)
def create_store(payload: StoreCreate, service: StoreService = Depends(get_store_service)):
    return service.create_store(payload)


@router.put("/{store_id}", response_model=StoreOut)
def update_store(
    store_id: int,
    payload: StoreUpdate,
    service: StoreService = Depends(get_store_service),
):
    updated = service.update_store(store_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Store not found")
    return updated


@router.delete("/{store_id}", status_code=204)
def delete_store(store_id: int, service: StoreService = Depends(get_store_service)):
    deleted = service.delete_store(store_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Store not found")
    return None
