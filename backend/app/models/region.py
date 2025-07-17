import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.schemas.region import RegionBase

if TYPE_CHECKING:
    from app.models.site import Site


# Database model, database table inferred from class name
class Region(RegionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    site_id: uuid.UUID = Field(
        foreign_key="site.id", nullable=False, ondelete="CASCADE"
    )
    site: "Site" = Relationship(back_populates="regions")
