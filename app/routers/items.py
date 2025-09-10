from typing import Optional

from fastapi import APIRouter, Query, status

from ..schemas import ItemCreate, ItemUpdate, ItemOut, PaginatedItems
from .. import crud

router = APIRouter()


@router.post("/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item_endpoint(payload: ItemCreate):
    item = await crud.create_item(payload)
    return item


@router.get("/", response_model=PaginatedItems)
async def list_items_endpoint(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    title: Optional[str] = Query(default=None),
):
    total, items = await crud.list_items(limit=limit, offset=offset, title=title)
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/{item_id}", response_model=ItemOut)
async def get_item_endpoint(item_id: int):
    return await crud.get_item(item_id)


@router.put("/{item_id}", response_model=ItemOut)
async def update_item_endpoint(item_id: int, payload: ItemUpdate):
    return await crud.update_item(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_endpoint(item_id: int):
    await crud.delete_item(item_id)
    return None 