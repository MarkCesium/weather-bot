from pydantic_settings import BaseSettings
from aiogram import Bot, Dispatcher
import aioredis


class Config(BaseSettings):
    bot: Bot | None = None
    dp: Dispatcher | None = None

    BOT_TOKEN: str
    WEATHER_TOKEN: str
    redis_url: str = "redis://localhost:6379"


config = Config()
config.bot = Bot(config.BOT_TOKEN)
config.dp = Dispatcher()

redis = aioredis.from_url(config.redis_url)
