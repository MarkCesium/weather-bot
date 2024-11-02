from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core import Params
from services import (
    get_response_text,
    get_weather,
    get_weather_cache,
    set_weather_cache,
)
from keyboards.inline_keyboard import get_ikb

router: Router = Router()


@router.message(F.text | F.location)
async def broadcast(message: Message, state: FSMContext):
    if message.location is not None:
        lon: float = message.location.longitude
        lat: float = message.location.latitude
        params = Params(location=(lat, lon))
    else:
        city: str = message.text
        params = Params(city=city)

    cache: str | None = await get_weather_cache(params)

    if cache is not None:
        if params.q is not None:
            await state.update_data({"last_city": params.q})
        else:
            await state.update_data({"last_location": (params.lat, params.lon)})
        await message.answer(cache, reply_markup=await get_ikb(state))
        return

    data = await get_weather(params)
    if data is None:
        await message.answer(
            "Oops, something went wrong! Try again later or check the city name",
            reply_markup=await get_ikb(state),
        )
        return

    text = await get_response_text(
        data["weather"][0]["description"],
        data["main"]["temp"],
        data["main"]["feels_like"],
        data["wind"]["speed"],
        data["main"]["humidity"],
    )
    await set_weather_cache(params, text)
    if params.q is not None:
        await state.update_data({"last_city": params.q})
    else:
        await state.update_data({"last_location": (params.lat, params.lon)})
    await message.answer(text, reply_markup=await get_ikb(state))


@router.callback_query(F.data)
async def broadcast_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    state_data = await state.get_data()
    try:
        if callback_query.data == "last_city":
            params = Params(city=state_data.get("last_city"))
        else:
            print("location")
            params = Params(location=state_data.get("last_location"))
    except:
        await callback_query.message.answer("Server has no data about the last request")
        return

    cache: str | None = await get_weather_cache(params)
    if cache is not None:
        await callback_query.message.answer(cache, reply_markup=await get_ikb(state))
        return

    data = await get_weather(params)
    if data is None:
        await callback_query.message.answer(
            "Oops, something went wrong! Try again later or check the city name",
            reply_markup=await get_ikb(state),
        )
        return

    text = await get_response_text(
        data["weather"][0]["description"],
        data["main"]["temp"],
        data["main"]["feels_like"],
        data["wind"]["speed"],
        data["main"]["humidity"],
    )
    await set_weather_cache(params, text)
    await callback_query.message.answer(text, reply_markup=await get_ikb(state))
    await callback_query.message.delete()
