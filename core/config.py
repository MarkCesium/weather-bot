from pydantic_settings import BaseSettings
from aiogram import Bot, Dispatcher

from redis import asyncio as aioredis


class Config(BaseSettings):
    bot: Bot | None = None
    dp: Dispatcher | None = None
    redis: aioredis.Redis | None = None

    BOT_TOKEN: str
    WEATHER_TOKEN: str
    redis_url: str = "redis://localhost:6379"


config = Config()
config.bot = Bot(config.BOT_TOKEN)
config.dp = Dispatcher()


@config.dp.startup()
async def on_startup():
    config.redis = aioredis.from_url(config.redis_url)


@config.dp.shutdown()
async def on_shutdown():
    await config.redis.close()
