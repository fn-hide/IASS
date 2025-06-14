from fastapi_utils.tasks import repeat_every
from sqlmodel import Session, create_engine

from app.core.config import settings
from app.main import app
from app.repositories.r_item import RItem
from app.schemas import ItemCreate
from app.services.s_item import SItem
from app.utils import create_edge_user, is_hub_up, send_item


@app.on_event("startup")
async def register_edge_user():
    return await create_edge_user()


@app.on_event("startup")
@repeat_every(seconds=1)
async def ping_hub():
    if await is_hub_up():
        return await send_item()
    return None


# -- development only --
@app.on_event("startup")
@repeat_every(seconds=1)
async def insert_item():
    from app.repositories.r_user import RUser
    from app.services.s_user import SUser
    from app.utils import utcnow

    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    with Session(engine) as session:
        repository = RUser(session)
        service = SUser(repository)
        user = service.read_users(skip=0, limit=1)

        repository = RItem(session)
        service = SItem(repository)
        # NOTE: Generate fake data on edge device
        item = ItemCreate(
            date_stamped=utcnow(),
            entity_index=1,
            is_in=True,
            is_up=False,
        )
        return await service.create_item(item, user.data[0].id)
