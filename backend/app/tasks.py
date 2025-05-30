from fastapi_utils.tasks import repeat_every

from app.main import app
from app.utils import is_hub_up


@app.on_event("startup")
@repeat_every(seconds=1)
async def ping_hub():
    return await is_hub_up()
