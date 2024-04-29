from typing import Awaitable, Callable

from fastapi import FastAPI
from loguru import logger

from axegaoshop.services.crons.clear_database import clear_amount_of_purchasing

from apscheduler.schedulers.asyncio import AsyncIOScheduler

async_scheduler = AsyncIOScheduler()


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:
    """
    События, вызывающиеся при начале работы нашего приложения

     - Удаление "старых" запросов на пополнение/покупку товара
    """

    @app.on_event("startup")
    async def _startup() -> None:
        async_scheduler.add_job(
            clear_amount_of_purchasing, "interval", seconds=4, misfire_grace_time=10
        )

        logger.info("Cache initialized")

        async_scheduler.start()

    return _startup
