import aiohttp
from src.core import Params


async def get_weather(params: Params) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.openweathermap.org/data/2.5/weather", params=await params()
        ) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()

    return data
