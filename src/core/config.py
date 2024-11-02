from pydantic_settings import BaseSettings
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from redis import asyncio as aioredis


class Config(BaseSettings):
    bot: Bot | None = None
    dp: Dispatcher | None = None
    redis: aioredis.Redis | None = None

    BOT_TOKEN: str
    WEATHER_TOKEN: str
    redis_url: str
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_USER_PASSWORD: str

    class Config:
        env_file = ".env"


config = Config()
config.bot = Bot(config.BOT_TOKEN)
storage = RedisStorage.from_url(config.redis_url + "/0")
config.dp = Dispatcher(storage=storage)


@config.dp.startup()
async def on_startup():
    config.redis = aioredis.from_url(config.redis_url + "/1")


@config.dp.shutdown()
async def on_shutdown():
    await config.redis.close()
