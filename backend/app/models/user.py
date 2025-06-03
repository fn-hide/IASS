import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.schemas.user import UserBase

if TYPE_CHECKING:
    from app.models.hub import Hub
    from app.models.item import Item
    from app.models.site import Site


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    sites: list["Site"] = Relationship(back_populates="owner", cascade_delete=True)
    hubs: list["Hub"] = Relationship(back_populates="owner", cascade_delete=True)
