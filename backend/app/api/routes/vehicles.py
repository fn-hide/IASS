import uuid
from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import SessionDep, get_current_active_superuser
from app.models import Message
from app.repositories import RHub, RSite
from app.services import SHub, SSite, SVehicle

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
)
def read_jobs() -> Any:
    """
    Retrieve jobs.
    """

    svehicle = SVehicle()
    return svehicle.read_jobs()


@router.post(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
)
def create_job(session: SessionDep, id: uuid.UUID, verbose: int = 0) -> Any:
    """
    Create a new job.
    """

    rhub = RHub(session)
    shub = SHub(rhub)

    rsite = RSite(session)
    ssite = SSite(rsite)

    svehicle = SVehicle(shub, ssite)
    return svehicle.create_job(id, verbose)


@router.delete("/{id}", dependencies=[Depends(get_current_active_superuser)])
def delete_job(session: SessionDep, id: uuid.UUID) -> Message:
    """
    Delete a job.
    """

    rhub = RHub(session)
    shub = SHub(rhub)

    rsite = RSite(session)
    ssite = SSite(rsite)

    svehicle = SVehicle(shub, ssite)
    return svehicle.delete_job(id)
