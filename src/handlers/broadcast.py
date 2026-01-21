from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from dishka.integrations.aiogram import FromDishka

from src.core.config import Settings
from src.models import Params
from src.services.weather import WeatherService

router: Router = Router()


@router.message(F.text | F.location)
async def broadcast(
    message: Message,
    state: FSMContext,
    settings: FromDishka[Settings],
    weather_service: FromDishka[WeatherService],
):
    if message.location is not None:
        params = Params(
            appid=settings.weather.token,
            location=(message.location.latitude, message.location.longitude),
        )
    elif message.text is not None:
        params = Params(appid=settings.weather.token, city=message.text)
    else:
        await message.answer("Something went wrong")
        return

    await weather_service.get_broadcast(message, state, params)


@router.callback_query(F.data)
async def broadcast_callback(
    callback_query: CallbackQuery,
    state: FSMContext,
    settings: FromDishka[Settings],
    weather_service: FromDishka[WeatherService],
):
    await callback_query.answer()
    if callback_query.message is None:
        return
    message = callback_query.message
    state_data = await state.get_data()
    try:
        if callback_query.data == "last_city":
            city: str | None = state_data.get("last_city")
            if city is None:
                raise ValueError
            params = Params(appid=settings.weather.token, city=city)
        else:
            location: tuple | list | None = state_data.get("last_location")
            if location is None:
                raise ValueError
            params = Params(appid=settings.weather.token, location=location)
    except ValueError:
        await message.answer("Server has no data about the last request")
        return

    await weather_service.get_broadcast(message, state, params)

    if not isinstance(message, InaccessibleMessage):
        await message.delete()
