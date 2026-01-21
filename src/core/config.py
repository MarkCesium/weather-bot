import logging
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class LoggingConfig(BaseModel):
    level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    format: str = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.level.upper()]


class TelegramConfig(BaseModel):
    token: str = Field(...)


class WeatherAPIConfig(BaseModel):
    token: str = Field(...)


class RedisConfig(BaseModel):
    url: str = Field(...)


class Settings(BaseSettings):
    logging: LoggingConfig = Field(...)
    telegram: TelegramConfig = Field(...)
    weather: WeatherAPIConfig = Field(...)
    redis: RedisConfig = Field(...)

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
