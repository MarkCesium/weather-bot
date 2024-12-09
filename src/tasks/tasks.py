from src.core.config import config
from src.core.params import Params
from src.services import get_weather, get_response_text
from src.services.cache import get_weather_cache, set_weather_cache
from .celery import celery


@celery.task()
async def send_notification(user_id: int, key: str, city: bool):
    if city:
        params = Params(city=key)
    else:
        params = Params(location=key)

    cache: str | None = await get_weather_cache(params)

    if cache is not None:
        await config.bot.send_message(chat_id=user_id, text=cache)
        return

    data = await get_weather(params)

    if data is None:
        await config.bot.send_message(
            chat_id=user_id,
            text="Oops, something went wrong! We cannot send you a notification",
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

    await config.bot.send_message(chat_id=user_id, text=cache)
