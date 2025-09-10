from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)


class ItemOut(ItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedItems(BaseModel):
    total: int
    items: List[ItemOut]
    limit: int
    offset: int 