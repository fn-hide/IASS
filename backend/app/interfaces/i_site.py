import uuid
from abc import ABC

from app.models import Site

from .i_base import IBase


class ISite(IBase[Site, uuid.UUID], ABC):
    pass
