from .name_broadcast import router as broadcast_by_name_router
from .start import router as start_router
from .location_broadcast import router as broadcast_by_location_router
from aiogram import Router

routers: tuple[Router] = (
    start_router,
    broadcast_by_location_router,
    broadcast_by_name_router,
)
