import asyncio

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

from config import BOT_TOKEN
from handlers import start_router, name_router, location_router


async def main():
    bot: Bot = Bot(BOT_TOKEN)
    dp: Dispatcher = Dispatcher()
    dp.include_routers(start_router, location_router, name_router)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
