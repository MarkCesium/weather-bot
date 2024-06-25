from aiogram import Router, F
from aiogram.types import Message
from config import Params
from services import get_response_text, get_weather

router: Router = Router()


@router.message(F.location)
async def location_broadcast(message: Message):
    lon: float = message.location.longitude
    lat: float = message.location.latitude
    params = Params(location=(lat, lon))

    data = await get_weather(params, message)

    await message.answer(
        text=get_response_text(
            data["weather"][0]["description"],
            data["main"]["temp"],
            data["main"]["feels_like"],
            data["wind"]["speed"],
            data["main"]["humidity"],
        )
    )
