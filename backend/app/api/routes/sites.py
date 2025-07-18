import uuid
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import Message
from app.repositories import RSite
from app.schemas import (
    SiteCreate,
    SitePublic,
    SiteRegionsPublic,
    SitesPublic,
    SiteUpdate,
)
from app.services import SSite

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SitesPublic,
)
def read_sites(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve sites.
    """

    repository = RSite(session=session)
    service = SSite(repository=repository)
    return service.read_sites(skip=skip, limit=limit)


@router.get("/{id}/sample")
def read_site_sample(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get site sample by ID.
    """

    repository = RSite(session=session)
    service = SSite(repository=repository)
    buffer = service.read_site_sample(id=id)
    frame_bytes = buffer.tobytes()
    return Response(content=frame_bytes, media_type="image/jpeg")


@router.get(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SitePublic,
)
def read_site(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get site by ID.
    """

    repository = RSite(session=session)
    service = SSite(repository=repository)
    return service.read_site(id=id)


@router.get(
    "/{id}/regions",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SiteRegionsPublic,
)
def read_site_with_regions(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get site with regions by ID.
    """

    repository = RSite(session)
    service = SSite(repository)
    return service.read_site_with_regions(id)


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=SitePublic
)
def create_site(
    *, session: SessionDep, current_user: CurrentUser, site_in: SiteCreate
) -> Any:
    """
    Create a new site.
    """

    repository = RSite(session=session)
    service = SSite(repository=repository)
    return service.create_site(site_in=site_in, user_id=current_user.id)


@router.put(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SitePublic,
)
def update_site(*, session: SessionDep, id: uuid.UUID, site_in: SiteUpdate) -> Any:
    """
    Update an site.
    """

    repository = RSite(session=session)
    service = SSite(repository=repository)
    return service.update_site(id=id, site_in=site_in)


@router.delete("/{id}", dependencies=[Depends(get_current_active_superuser)])
def delete_site(session: SessionDep, id: uuid.UUID) -> Message:
    """
    Delete an site.
    """

    repository = RSite(session=session)
    service = SSite(repository=repository)
    return service.delete_site(id=id)
