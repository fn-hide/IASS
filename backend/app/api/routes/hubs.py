import uuid
from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import Message
from app.repositories import RHub
from app.schemas import (
    HubCreate,
    HubPublic,
    HubsPublic,
    HubUpdate,
)
from app.services import SHub

router = APIRouter(prefix="/hubs", tags=["hubs"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=HubsPublic,
)
def read_hubs(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve hubs.
    """

    repository = RHub(session=session)
    service = SHub(repository=repository)
    return service.read_hubs(skip=skip, limit=limit)


@router.get(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=HubPublic,
)
def read_hub(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get hub by ID.
    """

    repository = RHub(session=session)
    service = SHub(repository=repository)
    return service.read_hub(id=id)


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=HubPublic
)
def create_hub(
    *, session: SessionDep, current_user: CurrentUser, hub_in: HubCreate
) -> Any:
    """
    Create a new hub.
    """

    repository = RHub(session=session)
    service = SHub(repository=repository)
    return service.create_hub(hub_in=hub_in, user_id=current_user.id)


@router.put(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=HubPublic,
)
def update_hub(*, session: SessionDep, id: uuid.UUID, hub_in: HubUpdate) -> Any:
    """
    Update an hub.
    """

    repository = RHub(session=session)
    service = SHub(repository=repository)
    return service.update_hub(id=id, hub_in=hub_in)


@router.delete("/{id}", dependencies=[Depends(get_current_active_superuser)])
def delete_hub(session: SessionDep, id: uuid.UUID) -> Message:
    """
    Delete an hub.
    """

    repository = RHub(session=session)
    service = SHub(repository=repository)
    return service.delete_hub(id=id)
