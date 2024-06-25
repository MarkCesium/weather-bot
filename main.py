import asyncio

from aiogram import Bot, Dispatcher

from aiogram.methods import DeleteWebhook

from config import BOT_TOKEN
from handlers import routers


async def main():
    bot: Bot = Bot(BOT_TOKEN)
    dp: Dispatcher = Dispatcher()
    dp.include_routers(*routers)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
