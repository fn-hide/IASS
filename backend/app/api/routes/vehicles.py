import uuid
from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import SessionDep, get_current_active_superuser
from app.repositories import RSite
from app.services import SSite, SVehicle

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get(
    "/jobs",
    dependencies=[Depends(get_current_active_superuser)],
)
def read_jobs() -> Any:
    """
    Retrieve jobs.
    """

    svehicle = SVehicle()
    return svehicle.read_jobs()


@router.post(
    "/{id}/start",
    dependencies=[Depends(get_current_active_superuser)],
)
def start_job(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Start a specific "job" i.e. vehicle counting.
    """

    rsite = RSite(session)
    ssite = SSite(rsite)
    svehicle = SVehicle(ssite)
    return svehicle.start_job(id)
