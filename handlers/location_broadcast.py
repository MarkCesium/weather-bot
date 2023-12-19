from aiogram import Router, F
from aiogram.types import Message
import aiohttp
from config import WEATHER_TOKEN

location_router: Router = Router()


@location_router.message(F.location)
async def location_broadcast(message: Message):
    lon: float = message.location.longitude
    lat: float = message.location.latitude
    params = {
        'units': 'metric',
        'lang': 'ru',
        'appid': WEATHER_TOKEN,
        'lat': lat,
        'lon': lon
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
                'https://api.openweathermap.org/data/2.5/weather',
                params=params
        ) as resp:
            if resp.status != 200:
                await message.answer('Штосьці здарылася?? Сервер не працуе, паспрабуйце ледзь пазьней!')
                resp.close()
                return

            data = await resp.json()
            await message.answer(
                text=f'Зараз за акенцам {data["weather"][0]["description"]}\nТэмпература {data["main"]["temp"]},\
 але адчуваецца як {data["main"]["feels_like"]}\nХуткасьць ветру {data["wind"]["speed"]} м/с\
\nВільготнасьць {data["main"]["humidity"]}%'
            )
            resp.close()
