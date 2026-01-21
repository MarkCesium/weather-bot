from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.keyboards.main_keyboard import get_main_kb

router: Router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        text="Hi! It's the Weather Bot. Type in the name of the city or use the button.",
        reply_markup=await get_main_kb(),
    )
