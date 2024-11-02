from .start import router as start_router
from .broadcast import router as broadcast_router
from aiogram import Router

routers: tuple[Router] = (
    start_router,
    broadcast_router,
)
