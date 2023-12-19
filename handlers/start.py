from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_router: Router = Router()


@start_router.message(Command('start'))
async def start(message: Message):
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Бягучая лакацацыя", request_location=True)
    )
    await message.answer(
        text='Вітанкі! Гэта Надвор\'е бот. Напішы назву горада ці скарыстайся кнопкай',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
