from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router: Router = Router()


@router.message(Command("start"))
async def start(message: Message):
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Current location", request_location=True))
    await message.answer(
        text="Hi! It's the Weather Bot. Type in the name of the city or use the button.",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
