import uuid
from abc import ABC

from app.models import Region

from .i_base import IBase


class IRegion(IBase[Region, uuid.UUID], ABC):
    pass
