from redis.asyncio import client

from src.core import Params


class CacheService:
    def __init__(self, client: client.Redis):
        self.client = client

    async def get_weather(self, params: Params) -> str | None:
        return await self.client.get(params.cache_key())

    async def set_weather_cache(self, params: Params, data: str) -> None:
        await self.client.setex(params.cache_key(), 600, data)
