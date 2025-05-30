import uuid
from abc import ABC

from app.models import Hub

from .i_base import IBase


class IHub(IBase[Hub, uuid.UUID], ABC):
    pass
