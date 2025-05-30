import uuid
from abc import ABC

from app.models import Item

from .i_base import IBase


class IItem(IBase[Item, uuid.UUID], ABC):
    pass
