import uuid
from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import Message
from app.repositories import RItem
from app.schemas import (
    ItemCreate,
    ItemPublic,
    ItemsPublic,
)
from app.services import SItem

router = APIRouter(prefix="/items", tags=["items"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ItemsPublic,
)
def read_items(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve items.
    """

    repository = RItem(session=session)
    service = SItem(repository=repository)
    return service.read_items(skip=skip, limit=limit)


@router.get(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ItemPublic,
)
def read_item(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get item by ID.
    """

    repository = RItem(session=session)
    service = SItem(repository=repository)
    return service.read_item(id=id)


@router.post("/", response_model=ItemPublic)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    """
    Create a new item.
    """

    repository = RItem(session=session)
    service = SItem(repository=repository)
    return service.create_item(item_in=item_in, user_id=current_user.id)


@router.delete("/{id}", dependencies=[Depends(get_current_active_superuser)])
def delete_item(session: SessionDep, id: uuid.UUID) -> Message:
    """
    Delete an item.
    """

    repository = RItem(session=session)
    service = SItem(repository=repository)
    return service.delete_item(id=id)
