from aiogram import Router, F
from aiogram.types import Message
from core import Params
from services import (
    get_response_text,
    get_weather,
    get_weather_cache,
    set_weather_cache,
)

router: Router = Router()


@router.message(F.text | F.location)
async def broadcast(message: Message):
    if message.location is not None:
        lon: float = message.location.longitude
        lat: float = message.location.latitude
        params = Params(location=(lat, lon))
    else:
        city: str = message.text
        params = Params(city=city)

    cache: str | None = await get_weather_cache(params)

    if cache is not None:
        await message.answer(cache)
        return

    data = await get_weather(params)
    if data is None:
        await message.answer(
            "Oops, something went wrong! Try again later or check the city name"
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
    await message.answer(text)
