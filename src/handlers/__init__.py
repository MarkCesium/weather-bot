from aiogram import Router

from src.handlers.broadcast import router as broadcast_router
from src.handlers.start import router as start_router

routers: tuple[Router, ...] = (
    start_router,
    broadcast_router,
)
