import aiohttp
from dishka import Provider, Scope, provide

from src.services.cache import CacheService
from src.services.weather import WeatherService


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_weather_service(
        self, session: aiohttp.ClientSession, cache_service: CacheService
    ) -> WeatherService:
        return WeatherService(session=session, cache_service=cache_service)
