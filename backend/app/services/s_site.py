import uuid

import cv2 as cv
from fastapi import HTTPException

from app.models import Message, Site
from app.repositories import RSite
from app.schemas import SiteCreate, SiteRegionsPublic, SitesPublic, SiteUpdate


class SSite:
    def __init__(self, repository: RSite | None = None) -> None:
        self.repository = repository

    def read_sites(self, skip=0, limit=10) -> SitesPublic:
        objs = self.repository.list(skip=skip, limit=limit)
        count = self.repository.count()
        return SitesPublic(data=objs, count=count)

    def read_site(self, id: uuid.UUID) -> Site:
        obj = self.repository.get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Site not found")
        return obj

    def read_site_with_regions(self, id: uuid.UUID) -> SiteRegionsPublic:
        obj = self.repository.get_site_with_regions(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Site not found")
        return obj

    def read_site_sample(self, id: uuid.UUID) -> Site:
        obj = self.read_site(id)
        url = f"rtsp://{obj.username}:{obj.password}@{obj.host}:{obj.port}"
        cap = cv.VideoCapture(url)
        ret, frame = cap.read()
        if not ret:
            return Message(message="Failed to get sample of the CCTV site.")
        cap.release()
        _, buffer = cv.imencode(".jpg", frame)
        return buffer

    def create_site(self, site_in: SiteCreate, user_id: uuid.UUID) -> Site:
        obj = Site.model_validate(site_in, update={"owner_id": user_id})
        return self.repository.create(obj)

    def update_site(self, id: uuid.UUID, site_in: SiteUpdate) -> Site:
        site_obj = self.read_site(id=id)
        update_dict = site_in.model_dump(exclude_unset=True)
        return self.repository.update(obj=site_obj, data=update_dict)

    def delete_site(self, id: uuid.UUID) -> Message:
        site_obj = self.read_site(id=id)
        self.repository.delete(site_obj)
        return Message(message="Site deleted successfully")
