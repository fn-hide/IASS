import os
import uuid

from fastapi import HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings
from app.models import Hub, Message
from app.repositories import RHub
from app.schemas import HubCreate, HubsPublic, HubUpdate


class SHub:
    def __init__(self, repository: RHub | None = None) -> None:
        self.repository = repository

    def read_hubs(self, skip=0, limit=10) -> HubsPublic:
        objs = self.repository.list(skip=skip, limit=limit)
        count = self.repository.count()
        return HubsPublic(data=objs, count=count)

    def read_hub(self, id: uuid.UUID) -> Hub:
        obj = self.repository.get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Hub not found")
        return obj

    def create_hub(self, hub_in: HubCreate, user_id: uuid.UUID) -> Hub:
        obj = Hub.model_validate(hub_in, update={"owner_id": user_id})
        return self.repository.create(obj)

    def update_hub(self, id: uuid.UUID, hub_in: HubUpdate) -> Hub:
        hub_obj = self.read_hub(id=id)
        update_dict = hub_in.model_dump(exclude_unset=True)
        return self.repository.update(obj=hub_obj, data=update_dict)

    def delete_hub(self, id: uuid.UUID) -> Message:
        hub_obj = self.read_hub(id=id)
        self.repository.delete(hub_obj)
        return Message(message="Hub deleted successfully")

    def download_model(self) -> FileResponse | Message:
        hub = self.read_hubs().data[0]
        model_path = os.path.join(settings.DIR_ASSETS, hub.model)
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Hub not found")
        return FileResponse(
            path=os.path.join(settings.DIR_ASSETS, hub.model),
            filename=hub.model,
            media_type="application/octet-stream",
        )
