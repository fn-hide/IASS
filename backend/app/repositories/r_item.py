import uuid

from sqlmodel import Session

from app.interfaces import IItem
from app.models import Item
from app.repositories import RBase


class RItem(RBase[Item, uuid.UUID], IItem):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Item)
