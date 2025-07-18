from sqlmodel import Session, select

from app import crud
from app.core.config import settings
from app.models import Hub, Site, User
from app.repositories import RHub, RSite
from app.schemas import HubCreate, SiteCreate, UserCreate
from app.services import SHub, SSite


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables uncommenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

    hub = session.exec(select(Hub).where(Hub.name == settings.DEFAULT_HUB_NAME)).first()
    if not hub:
        hub_in = HubCreate(
            name=settings.DEFAULT_HUB_NAME,
            address=settings.DEFAULT_HUB_ADDRESS,
            latitude=settings.DEFAULT_HUB_LATITUDE,
            longitude=settings.DEFAULT_HUB_LONGITUDE,
            host=settings.DEFAULT_HUB_HOST,
            port=settings.DEFAULT_HUB_PORT,
            sync_interval=settings.DEFAULT_HUB_SYNC_INTERVAL,
            sync_size=settings.DEFAULT_HUB_SYNC_SIZE,
            model=settings.DEFAULT_HUB_MODEL,
        )
        repository = RHub(session)
        service = SHub(repository)
        service.create_hub(hub_in=hub_in, user_id=user.id)

    # --- development --- #
    site = session.exec(select(Site).where(Site.name == "main")).first()
    if not site:
        site_in = SiteCreate(
            name="main",
            latitude=0,
            longitude=0,
            username="huda",
            password="Burunghudhud112",
            host="192.168.50.26",
            port="554",
            line_in="[[839, 20], [1157, 1333]]",
            line_out="[[839, 20], [1157, 1333]]",
            polygon="[[1157, 72], [1516, 278], [854, 1101], [707, 146]]",
        )
        repository = RSite(session)
        service = SSite(repository)
        service.create_site(site_in=site_in, user_id=user.id)
