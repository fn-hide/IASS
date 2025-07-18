import uuid
from abc import ABC, abstractmethod

from app.models import Site

from .i_base import ID, IBase, T


class ISite(IBase[Site, uuid.UUID], ABC):
    @abstractmethod
    def get_site_with_regions(self, id: ID) -> T:
        ...
