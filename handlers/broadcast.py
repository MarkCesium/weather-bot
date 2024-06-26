from aiogram import Router, F
from aiogram.types import Message
from core import Params
from services import get_response_text, get_weather

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

    status, data = await get_weather(params, message)
    if not status:
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
    await message.answer(text=text)
