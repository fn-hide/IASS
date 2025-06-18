import uuid
from datetime import datetime

from sqlmodel import Field

from app.models.base import BaseModel

from .utils import utcnow


# Shared properties
class ItemBase(BaseModel):
    date_created: datetime = Field(default_factory=utcnow)
    date_stamped: datetime
    id_track: int
    id_cls: int
    is_out: bool
    is_up: bool


class ItemCreate(ItemBase):
    pass


class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(BaseModel):
    data: list[ItemPublic]
    count: int
