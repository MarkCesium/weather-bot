from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()


class Notifications(StatesGroup):
    base = State()
    time = State()
    apply = State()


@router.message(Command("notify"))
async def notifications_base(message: Message, state: FSMContext):
    await message.answer(
        "Please, type in the city or location you want to get notifications about"
    )
    await Notifications.base.set()


@router.message(F.text | F.location, state=Notifications.base)
async def notifications_get_place(
    message: Message, state: FSMContext
): ...  # TODO: test place by getting weather and save it in state


@router.message(F.text, state=Notifications.time)
async def notifications_get_time(
    message: Message, state: FSMContext
): ...  # TODO: match time by regex, save it in state, return ikb yes/no


@router.callback_query()
async def notifications_apply(
    callback_query: CallbackQuery, state: FSMContext
): ...  # TODO: check apply, if apply - call task
