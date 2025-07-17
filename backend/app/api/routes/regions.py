import uuid
from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import SessionDep, get_current_active_superuser
from app.models import Message
from app.repositories import RRegion, RSite
from app.schemas import (
    RegionCreate,
    RegionPublic,
    RegionsPublic,
    RegionUpdate,
)
from app.services import SRegion, SSite

router = APIRouter(prefix="/regions", tags=["regions"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RegionsPublic,
)
def read_regions(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve regions.
    """

    repository = RRegion(session=session)
    service = SRegion(repository=repository)
    return service.read_regions(skip=skip, limit=limit)


@router.get(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RegionPublic,
)
def read_region(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get region by ID.
    """

    repository = RRegion(session=session)
    service = SRegion(repository=repository)
    return service.read_region(id=id)


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RegionPublic,
)
def create_region(*, session: SessionDep, region_in: RegionCreate) -> Any:
    """
    Create a new region.
    """
    rsite = RSite(session)
    ssite = SSite(rsite)

    repository = RRegion(session)
    service = SRegion(repository, ssite)
    return service.create_region(region_in=region_in)


@router.put(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RegionPublic,
)
def update_region(
    *, session: SessionDep, id: uuid.UUID, region_in: RegionUpdate
) -> Any:
    """
    Update an region.
    """

    repository = RRegion(session=session)
    service = SRegion(repository=repository)
    return service.update_region(id=id, region_in=region_in)


@router.delete("/{id}", dependencies=[Depends(get_current_active_superuser)])
def delete_region(session: SessionDep, id: uuid.UUID) -> Message:
    """
    Delete an region.
    """

    repository = RRegion(session=session)
    service = SRegion(repository=repository)
    return service.delete_region(id=id)
