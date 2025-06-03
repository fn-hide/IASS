import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import emails  # type: ignore
import httpx
import jwt
from jinja2 import Template
from jwt.exceptions import InvalidTokenError
from pydantic import EmailStr
from sqlmodel import Session, create_engine, select

from app.core import security
from app.core.config import settings
from app.models import Hub, Item

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: EmailStr | str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logger.info(f"send email result: {response}")


def generate_test_email(email_to: EmailStr | str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(
    email_to: EmailStr | str, email: EmailStr | str, token: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.FRONTEND_HOST}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(
    email_to: EmailStr | str, username: EmailStr | str, password: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": settings.FRONTEND_HOST,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=security.ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        return str(decoded_token["sub"])
    except InvalidTokenError:
        return None


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def get_ping_hub_interval() -> int:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    with Session(engine) as session:
        stmt = select(Hub).limit(1)
        hub = session.exec(stmt).first()
        if not hub:
            return 1
        return hub.ping_hub_interval


async def is_hub_up() -> bool:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    with Session(engine) as session:
        stmt = select(Hub).limit(1)
        hub = session.exec(stmt).first()
    if not hub:
        logger.info("✖️ Hub not found")
        return False
    try:
        async with httpx.AsyncClient(timeout=1) as client:
            response = await client.get(str(hub.url))
            if response.status_code == 200:
                logger.info(f"⬆️ Hub is up: {response.status_code}")
                return True
            logger.info(f"⬇️ Hub is down: {response.status_code}")
            return False
    except httpx.ReadTimeout:
        logger.info("❌ Hub request failed: ReadTimeout")
        return False
    except httpx.ConnectTimeout:
        logger.info("❌ Hub request failed: ConnectTimeout")
        return False
    except Exception as e:
        logger.info(f"❌ Hub request failed with global exception: {str(e)}")
        return False


async def send_item() -> None:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    with Session(engine) as session:
        stmt = select(Hub).limit(1)
        hub = session.exec(stmt).first()
        if not hub:
            logger.info("✖️ Hub not found")
            return None
        stmt = select(Item).filter_by(is_up=False).limit(10)
        items = session.exec(stmt).all()
        if not items:
            logger.info("✅ Item is up-to-date. No need to send to hub.")
            return None
        async with httpx.AsyncClient() as client:
            url = "http://192.168.50.240:8000/api/v1/login/access-token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "username": settings.FIRST_SUPERUSER,
                "password": settings.FIRST_SUPERUSER_PASSWORD,
            }
            response = await client.post(url, data=data, headers=headers)
            if response.status_code != 200:
                logger.error("🚨 Token invalid!")
                return None
            token = response.json().get("access_token")
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
            }
            for item in items:
                data = {
                    "date_created": str(item.date_created),
                    "date_stamped": str(item.date_stamped),
                    "entity_index": item.entity_index,
                    "is_in": item.is_in,
                    "is_up": True,
                }
                try:
                    response = await client.post(
                        "http://192.168.50.240:8000/api/v1/items/",
                        headers=headers,
                        json=data,
                    )
                    if response.status_code == 200:
                        item.is_up = True
                        session.add(item)
                        logger.info("✔️ Sent item to hub")
                    else:
                        logger.warning(
                            f"❗ Failed to send item to hub: {response.status_code}"
                        )
                except Exception as e:
                    logger.error(f"❌ Exception while sending item to hub: {e}")
            session.commit()
            return None


async def create_edge_user() -> None:
    async with httpx.AsyncClient() as client:
        url = "http://192.168.50.240:8000/api/v1/users/signup"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {
            "email": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
            "full_name": "edge",
        }
        response = await client.post(url, headers=headers, json=data)
        if response.status_code != 200:
            logger.error("🚨 Failed to register a new edge user!")
        logger.error("🎉 Successfully registered a new edge user.")
        return None
