import uuid

from sqlmodel import Session

from app.interfaces import IHub
from app.models import Hub
from app.repositories import RBase


class RHub(RBase[Hub, uuid.UUID], IHub):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Hub)
