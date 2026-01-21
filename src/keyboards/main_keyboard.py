from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def get_main_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="Current location", request_location=True)).adjust(3)
    return kb.as_markup(resize_keyboard=True)
