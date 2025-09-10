from typing import List, Optional, Tuple

from fastapi import HTTPException, status

from .database import prisma
from .schemas import ItemCreate, ItemUpdate
from prisma.types import ItemWhereInput, ItemUpdateInput


async def create_item(data: ItemCreate) -> dict:
    try:
        async with prisma.tx() as tx:
            created = await tx.item.create(
                data={"title": data.title, "description": data.description}
            )
            await tx.item.update(
                where={"id": created.id},
                data={"description": created.description},
            )
            return created.dict()
    except Exception as exc:
        if "unique" in str(exc).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item with this title already exists",
            ) from exc
        raise


async def get_item(item_id: int) -> dict:
    item = await prisma.item.find_unique(where={"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.dict()


async def list_items(limit: int = 10, offset: int = 0, title: Optional[str] = None) -> Tuple[int, List[dict]]:
    where = None
    if title:
        where = {"title": {"contains": title, "mode": "insensitive"}}

    total = await prisma.item.count(where=where)
    rows = await prisma.item.find_many(
        where=where,
        skip=offset,
        take=limit,
    )

    await prisma.query_raw("SELECT COUNT(*) FROM \"Item\";")

    return total, [r.dict() for r in rows]


async def update_item(item_id: int, data: ItemUpdate) -> dict:
    existing = await prisma.item.find_unique(where={"id": item_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")

    payload = {}
    if data.title is not None:
        payload["title"] = data.title
    if data.description is not None:
        payload["description"] = data.description

    try:
        updated = await prisma.item.update(where={"id": item_id}, data=payload)
        return updated.dict()
    except Exception as exc:
        if "unique" in str(exc).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item with this title already exists",
            ) from exc
        raise


async def delete_item(item_id: int) -> None:
    try:
        await prisma.item.delete(where={"id": item_id})
    except Exception:
        existing = await prisma.item.find_unique(where={"id": item_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Item not found")
        raise
