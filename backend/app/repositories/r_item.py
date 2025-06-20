import uuid

from sqlmodel import Session, select

from app.interfaces import IItem
from app.models import Item
from app.repositories import RBase


class RItem(RBase[Item, uuid.UUID], IItem):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Item)

    def delete_by_condition(self, **conditions):
        stmt = select(self.model).filter_by(**conditions)
        results = self.session.exec(stmt).all()
        for obj in results:
            self.session.delete(obj)
        self.session.commit()
