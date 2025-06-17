from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import get_current_active_superuser
from app.services import SVehicle

router = APIRouter(prefix="/sites/vehicles", tags=["vehicles"])


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


@router.get(
    "/start_job",
    dependencies=[Depends(get_current_active_superuser)],
)
def start_job() -> Any:
    """
    Start job.
    """

    svehicle = SVehicle()
    return svehicle.start_job()
