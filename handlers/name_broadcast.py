from aiogram import Router
from aiogram.types import Message
import aiohttp
from config import WEATHER_TOKEN, Params
from services import get_response_text, get_weather

router: Router = Router()


@router.message()
async def name_broadcast(message: Message):
    city: str = message.text
    params = Params(city=city)

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
