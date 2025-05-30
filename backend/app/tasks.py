from fastapi_utils.tasks import repeat_every

from app.main import app
from app.utils import is_hub_up
from app.api.deps import SessionDep
from app.repositories.r_item import RItem
from app.services.s_item import SItem
from app.schemas import ItemCreate


@app.on_event("startup")
@repeat_every(seconds=1)
async def ping_hub():
    return await is_hub_up()


@app.on_event("startup")
@repeat_every(seconds=1)
async def insert_item():
    from app.utils import utcnow
    from app.repositories.r_user import RUser
    from app.services.s_user import SUser

    repository = RUser(SessionDep)
    service = SUser(repository)
    user = service.read_users(skip=0, limit=1)

    repository = RItem(SessionDep)
    service = SItem(repository)
    # NOTE: Generate fake data on edge device
    item = ItemCreate(
        date_stamped=utcnow(),
        entity_index=1,
        is_in=True,
        is_up=False,
    )
    return await service.create_item(item, user.data[0].id)
