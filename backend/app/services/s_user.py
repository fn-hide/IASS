import uuid

from fastapi import HTTPException

from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import Message, User
from app.repositories import RUser
from app.schemas import (
    UpdatePassword,
    UserCreate,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from app.utils import generate_new_account_email, send_email


class SUser:
    def __init__(self, repository: RUser) -> None:
        self.repository = repository

    def read_users(self, skip=0, limit=10) -> UsersPublic:
        objs = self.repository.list(skip, limit)
        count = self.repository.count()
        return UsersPublic(data=objs, count=count)

    def create_user(self, user_in: UserCreate | UserRegister) -> User:
        obj = self.repository.get_user_by_email(email=user_in.email)
        if obj:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )
        obj = User.model_validate(
            user_in, update={"hashed_password": get_password_hash(user_in.password)}
        )
        if settings.emails_enabled and user_in.email:
            email_data = generate_new_account_email(
                email_to=user_in.email,
                username=user_in.email,
                password=user_in.password,
            )
            send_email(
                email_to=user_in.email,
                subject=email_data.subject,
                html_content=email_data.html_content,
            )
        return self.repository.create(obj=obj)

    def update_user_me(self, current_user: User, user_in: UserUpdateMe):
        if user_in.email:
            existing_user = self.repository.get_user_by_email(user_in.email)
            if existing_user and existing_user.id != current_user.id:
                raise HTTPException(
                    status_code=409, detail="User with this email already exists"
                )
        update_dict = user_in.model_dump(exclude_unset=True)
        current_user.sqlmodel_update(update_dict)
        return self.repository.update(obj=current_user, data=update_dict)

    def update_password_me(self, current_user: User, body: UpdatePassword) -> Message:
        if not verify_password(body.current_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        if body.current_password == body.new_password:
            raise HTTPException(
                status_code=400,
                detail="New password cannot be the same as the current one",
            )
        hashed_password = get_password_hash(body.new_password)
        current_user.hashed_password = hashed_password
        self.repository.create(current_user)
        return Message(message="Password updated successfully")

    def delete_user_me(self, current_user: User) -> Message:
        if current_user.is_superuser:
            raise HTTPException(
                status_code=403,
                detail="Super users are not allowed to delete themselves",
            )
        self.repository.delete(obj=current_user)
        return Message(message="User deleted successfully")

    def register_user(self, user_in: UserRegister) -> User:
        user = self.repository.get_user_by_email(user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system",
            )
        return self.create_user(user_in=user_in)

    def read_user_by_id(self, id: uuid.UUID, current_user: User) -> User:
        user = self.repository.get(id)
        if user == current_user:
            return user
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=403,
                detail="The user doesn't have enough privileges",
            )
        return user

    def update_user(self, id: uuid.UUID, user_in: UserUpdate):
        db_user = self.repository.get(id)
        if not db_user:
            raise HTTPException(
                status_code=404,
                detail="The user with this id does not exist in the system",
            )
        if user_in.email:
            existing_user = self.repository.get_user_by_email(email=user_in.email)
            if existing_user and existing_user.id != id:
                raise HTTPException(
                    status_code=409, detail="User with this email already exists"
                )
        update_dict = user_in.model_dump(exclude_unset=True)
        return self.repository.update(obj=db_user, data=update_dict)

    def delete_user(self, id: uuid.UUID) -> Message:
        user = self.repository.get(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_superuser:
            raise HTTPException(
                status_code=403,
                detail="Super users are not allowed to delete themselves",
            )
        self.repository.delete(user)
        return Message(message="User deleted successfully")
