import asyncio
from aiogram.methods import DeleteWebhook
import logging
import sys
from core.config import config
from handlers import routers


async def main():
    bot = config.bot
    dp = config.dp

    dp.include_routers(*routers)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
