import uuid

from sqlmodel import Session

from app.interfaces import IRegion
from app.models import Region
from app.repositories import RBase


class RRegion(RBase[Region, uuid.UUID], IRegion):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Region)
