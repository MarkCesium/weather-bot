import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import InaccessibleMessage, Message

from src.keyboards.inline_keyboard import get_ikb
from src.models import Params
from src.services import CacheService


class WeatherService:
    def __init__(self, session: aiohttp.ClientSession, cache_service: CacheService):
        self.session = session
        self.cache_service = cache_service

    def get_response_text(
        self,
        description: str,
        temp: float,
        temp_feels_like: float,
        wind_speed: float,
        humidity: int,
    ) -> str:
        return f"""Right now there's {description} outside
🌡️ Temperature is {temp}, feels like {temp_feels_like}
💨 Wind speed {wind_speed} meters per second
💧 Humidity {humidity}%"""

    async def get_weather(self, params: Params) -> dict | None:
        async with self.session.get(
            "https://api.openweathermap.org/data/2.5/weather", params=params()
        ) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

    async def get_broadcast(
        self, message: Message | InaccessibleMessage, state: FSMContext, params: Params
    ):
        cache: str | None = await self.cache_service.get_weather(params)

        if cache is not None:
            if params.q is not None:
                await state.update_data({"last_city": params.q})
            else:
                await state.update_data({"last_location": (params.lat, params.lon)})
            await message.answer(cache, reply_markup=await get_ikb(state))
            return

        data = await self.get_weather(params)
        if data is None:
            await message.answer(
                "Oops, something went wrong! Try again later or check the city name",
                reply_markup=await get_ikb(state),
            )
            return

        text = self.get_response_text(
            data["weather"][0]["description"],
            data["main"]["temp"],
            data["main"]["feels_like"],
            data["wind"]["speed"],
            data["main"]["humidity"],
        )
        await self.cache_service.set_weather(params, text)
        if params.q is not None:
            await state.update_data({"last_city": params.q})
        else:
            await state.update_data({"last_location": (params.lat, params.lon)})
        await message.answer(text, reply_markup=await get_ikb(state))
