import uuid

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.interfaces import ISite
from app.models import Site
from app.repositories import RBase
from app.schemas import SiteRegionsPublic


class RSite(RBase[Site, uuid.UUID], ISite):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Site)

    def get_site_with_regions(self, id: uuid.UUID) -> SiteRegionsPublic | None:
        statement = (
            select(Site)
            .where(Site.id == id)
            .options(selectinload(Site.regions))  # eager load the regions
        )
        result = self.session.exec(statement).one_or_none()
        regions = [item.model_dump() for item in result.regions]
        result = result.model_dump()
        result["regions"] = {"data": regions, "count": len(regions)}
        return result
