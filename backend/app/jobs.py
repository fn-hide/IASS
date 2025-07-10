import logging

import httpx
from sqlmodel import select

from app.core.config import settings
from app.core.db import get_db
from app.models import Hub, Item

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def is_hub_up() -> bool:
    with get_db() as session:
        stmt = select(Hub).limit(1)
        hub = session.exec(stmt).first()
    if not hub:
        logger.info("✖️ Hub not found")
        return False
    async with httpx.AsyncClient(timeout=1) as client:
        try:
            url = f"http://{hub.host}:{hub.port}/api/v1/utils/health-check/"
            response = await client.get(url)
            if response.status_code == 200:
                logger.info(f"⬆️ Hub is up: {response.status_code}")
                return True
            logger.info(f"⬇️ Hub is down: {response.status_code}")
        except httpx.ReadTimeout:
            logger.info("❌ Hub request failed: ReadTimeout")
        except httpx.ConnectTimeout:
            logger.info("❌ Hub request failed: ConnectTimeout")
        except Exception as e:
            logger.info(f"❌ Hub request failed with global exception: {str(e)}")
        return False


async def send_item() -> None:
    with get_db() as session:
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
            url = f"http://{hub.host}:{hub.port}/api/v1/login/access-token"
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
                    "date_stamped": str(item.date_stamped),
                    "id_track": item.id_track,
                    "id_cls": item.id_cls,
                    "is_out": item.is_out,
                    "is_up": True,
                }
                try:
                    response = await client.post(
                        f"http://{hub.host}:{hub.port}/api/v1/items/",
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
    with get_db() as session:
        stmt = select(Hub).limit(1)
        hub = session.exec(stmt).first()
        if not hub:
            logger.info("✖️ Hub not found")
            return None
    async with httpx.AsyncClient() as client:
        url = f"http://{hub.host}:{hub.port}/api/v1/users/signup"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {
            "email": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
            "full_name": "edge",
        }
        try:
            response = await client.post(url, headers=headers, json=data)
            if response.status_code != 200:
                logger.error("🚨 Failed to register a new edge user!")
            else:
                logger.error("🎉 Successfully registered a new edge user.")
        except Exception as e:
            logger.error(
                f"❌ Raise global exception while create edge user in hub: {e}"
            )
    return None
