import uuid

from fastapi import HTTPException

from app.models import Message, Region
from app.repositories import RRegion
from app.schemas import RegionCreate, RegionsPublic, RegionUpdate


class SRegion:
    def __init__(self, repository: RRegion | None = None, ssite=None) -> None:
        self.repository = repository
        self.ssite = ssite

    def read_regions(self, skip=0, limit=10) -> RegionsPublic:
        objs = self.repository.list(skip=skip, limit=limit)
        count = self.repository.count()
        return RegionsPublic(data=objs, count=count)

    def read_region(self, id: uuid.UUID) -> Region:
        obj = self.repository.get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Region not found")
        return obj

    def create_region(self, region_in: RegionCreate) -> Region:
        if not self.ssite.read_site(region_in.site_id):
            raise HTTPException(status_code=404, detail="Site not found")
        obj = Region.model_validate(region_in)
        return self.repository.create(obj)

    def update_region(self, id: uuid.UUID, region_in: RegionUpdate) -> Region:
        region_obj = self.read_region(id=id)
        update_dict = region_in.model_dump(exclude_unset=True)
        return self.repository.update(obj=region_obj, data=update_dict)

    def delete_region(self, id: uuid.UUID) -> Message:
        region_obj = self.read_region(id=id)
        self.repository.delete(region_obj)
        return Message(message="Region deleted successfully")
