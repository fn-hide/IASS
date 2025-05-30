import uuid
from datetime import datetime

from sqlmodel import Field

from app.models.base import BaseModel
from app.utils import utcnow


# Shared properties
class ItemBase(BaseModel):
    date_created: datetime = Field(default_factory=utcnow)
    date_stamped: datetime
    entity_index: int
    is_in: bool


class ItemCreate(ItemBase):
    pass


class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(BaseModel):
    data: list[ItemPublic]
    count: int
