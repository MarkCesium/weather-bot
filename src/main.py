import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.methods import DeleteWebhook
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from src.core.config import Settings
from src.dependencies import (
    CacheProvider,
    ConfigProvider,
    HttpProvider,
    RedisProvider,
    ServiceProvider,
)
from src.handlers import routers


async def main():
    container = make_async_container(
        ConfigProvider(),
        RedisProvider(),
        CacheProvider(),
        HttpProvider(),
        ServiceProvider(),
    )
    settings = await container.get(Settings)

    logging.basicConfig(
        level=settings.logging.level_value,
        format=settings.logging.format,
        datefmt=settings.logging.date_format,
    )

    bot = Bot(settings.telegram.token)

    dp = Dispatcher(storage=RedisStorage.from_url(settings.redis.url + "/0"))
    dp.include_routers(*routers)

    setup_dishka(container=container, router=dp, auto_inject=True)
    dp.shutdown.register(container.close)

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
