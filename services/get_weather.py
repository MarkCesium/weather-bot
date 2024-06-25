import aiohttp
from aiogram.types import Message
from config import Params


async def get_weather(params: Params, message: Message) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.openweathermap.org/data/2.5/weather", params=params()
        ) as resp:
            if resp.status != 200:
                await message.answer(
                    "Oops, something went wrong! Try again later or check the city name"
                )
                await resp.close()
                return
            data = await resp.json()

    return data
