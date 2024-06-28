from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext


async def get_ikb(state: FSMContext) -> InlineKeyboardMarkup | None:
    ikb = InlineKeyboardBuilder()
    data = await state.get_data()
    counter: bool = False
    if data.get("last_city") is not None:
        ikb.add(
            InlineKeyboardButton(text="Last city", callback_data="last_city")
        ).adjust(2)
        counter = True

    if data.get("last_location") is not None:
        ikb.add(
            InlineKeyboardButton(text="Last location", callback_data="last_location")
        ).adjust(2)
        counter = True

    if counter is False:
        return None
    return ikb.as_markup()
