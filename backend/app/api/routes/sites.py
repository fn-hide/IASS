import uuid
from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import Message
from app.repositories import RSite
from app.schemas import (
    SiteCreate,
    SitePublic,
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
