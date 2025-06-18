import uuid
from abc import ABC, abstractmethod

from app.models import Item

from .i_base import IBase


class IItem(IBase[Item, uuid.UUID], ABC):
    @abstractmethod
    def delete_by_condition(self, **conditions) -> None:
        ...
