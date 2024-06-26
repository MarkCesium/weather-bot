import aiohttp
from aiogram.types import Message
from core import Params


async def get_weather(params: Params, message: Message) -> tuple[bool, dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.openweathermap.org/data/2.5/weather", params=await params()
        ) as resp:
            if resp.status != 200:
                return (False, {})
            data = await resp.json()

    return (True, data)
