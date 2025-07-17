import uuid

from app.models.base import BaseModel


# Shared properties
class RegionBase(BaseModel):
    line_in: str
    line_out: str
    polygon: str


# Properties to receive on item creation
class RegionCreate(RegionBase):
    pass


# Properties to receive on item update
class RegionUpdate(RegionBase):
    line_in: str | None  # type: ignore
    line_out: str | None  # type: ignore
    polygon: str | None  # type: ignore


# Properties to return via API, id is always required
class RegionPublic(RegionBase):
    id: uuid.UUID


class RegionsPublic(BaseModel):
    data: list[RegionPublic]
    count: int
