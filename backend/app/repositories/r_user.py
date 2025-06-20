import uuid

from pydantic import EmailStr
from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.interfaces import IUser
from app.models import User
from app.repositories import RBase


class RUser(RBase[User, uuid.UUID], IUser):
    def __init__(self, session: Session) -> None:
        super().__init__(session, User)

    def update(self, obj: User, data: dict) -> User:
        extra_data = {}
        if "password" in data:
            password = data["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashed_password"] = hashed_password
        obj.sqlmodel_update(data, update=extra_data)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_user_by_email(self, email: EmailStr | str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()
