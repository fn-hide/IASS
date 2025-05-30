import uuid

from sqlmodel import Field

from app.models.base import BaseModel


# Shared properties
class HubBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=255)
    latitude: float
    longitude: float
    url: str
    ping_hub_interval: int = Field(ge=1, le=60 * 60 * 24)


# Properties to receive on item creation
class HubCreate(HubBase):
    pass


# Properties to receive on item update
class HubUpdate(HubBase):
    name: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    address: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    latitude: float | None  # type: ignore
    longitude: float | None  # type: ignore
    url: str | None  # type: ignore
    ping_hub_interval: int | None  # type: ignore


# Properties to return via API, id is always required
class HubPublic(HubBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class HubsPublic(BaseModel):
    data: list[HubPublic]
    count: int
