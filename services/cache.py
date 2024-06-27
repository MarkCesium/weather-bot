from core.config import config
from core import Params


async def get_weather_cache(params: Params) -> str | None:
    return await config.redis.get(await params.cache_key())


async def set_weather_cache(params: Params, data: str) -> None:
    await config.redis.setex(await params.cache_key(), 300, data)
