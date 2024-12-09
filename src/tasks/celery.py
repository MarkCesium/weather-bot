from celery import Celery
from core.config import config

celery = Celery(
    "tasks",
    broker=config.rabbitmq_url,
    include=["src.tasks.tasks"],
)
