def get_response_text(
    description: str,
    temp: float,
    temp_feels_like: float,
    wind_speed: float,
    humidity: int,
) -> str:
    return f"""Right now there's {description} outside
Temperature is {temp}, feels like {temp_feels_like}.
Wind speed {wind_speed} meters per second.
Humidity {humidity}%."""
