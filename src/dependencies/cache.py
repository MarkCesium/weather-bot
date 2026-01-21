from dishka import Provider, Scope, provide
from redis.asyncio.client import Redis

from src.services.cache import CacheService


class CacheProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_cache_service(self, redis: Redis) -> CacheService:
        return CacheService(client=redis)
