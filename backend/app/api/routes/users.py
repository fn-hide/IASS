import uuid
from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.models import Message
from app.repositories import RUser
from app.schemas import (
    UpdatePassword,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from app.services import SUser

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """

    repository = RUser(session=session)
    service = SUser(repository=repository)
    return service.read_users(skip=skip, limit=limit)


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create a new user.
    """

    repository = RUser(session)
    service = SUser(repository)
    return service.create_user(user_in=user_in)


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    """
    Update own user.
    """

    repository = RUser(session)
    service = SUser(repository)
    return service.update_user_me(current_user=current_user, user_in=user_in)


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update own password.
    """

    repository = RUser(session)
    service = SUser(repository)
    return service.update_password_me(current_user=current_user, body=body)


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Delete own user.
    """

    repository = RUser(session)
    service = SUser(repository)
    return service.delete_user_me(current_user)


@router.post("/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create a new user without the need to be logged in.
    """

    repository = RUser(session)
    service = SUser(repository)
    return service.register_user(user_in=user_in)


@router.get("/{id}", response_model=UserPublic)
def read_user_by_id(
    id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """

    repository = RUser(session)
    service = SUser(repository)
    return service.read_user_by_id(id=id, current_user=current_user)


@router.patch(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update_user(*, session: SessionDep, id: uuid.UUID, user_in: UserUpdate) -> Any:
    """
    Update a user.
    """

    repository = RUser(session)
    service = SUser(repository)
    return service.update_user(id=id, user_in=user_in)


@router.delete("/{id}", dependencies=[Depends(get_current_active_superuser)])
def delete_user(session: SessionDep, id: uuid.UUID) -> Message:
    """
    Delete a user.
    """

    repository = RUser(session)
    service = SUser(repository)
    return service.delete_user(id=id)
