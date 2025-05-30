import uuid

from fastapi import HTTPException

from app.models import Item, Message
from app.repositories import RItem
from app.schemas import ItemCreate, ItemsPublic


class SItem:
    def __init__(self, repository: RItem | None = None) -> None:
        self.repository = repository

    def read_items(self, skip=0, limit=10) -> ItemsPublic:
        objs = self.repository.list(skip=skip, limit=limit)
        count = self.repository.count()
        return ItemsPublic(data=objs, count=count)

    def read_item(self, id: uuid.UUID) -> Item:
        obj = self.repository.get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Item not found")
        return obj

    def create_item(self, item_in: ItemCreate, user_id: uuid.UUID) -> Item:
        obj = Item.model_validate(item_in, update={"owner_id": user_id})
        return self.repository.create(obj)

    def delete_item(self, id: uuid.UUID) -> Message:
        item_obj = self.read_item(id=id)
        self.repository.delete(item_obj)
        return Message(message="Item deleted successfully")
