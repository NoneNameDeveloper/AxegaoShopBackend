from typing import Awaitable, Callable

from fastapi import FastAPI
from loguru import logger

from axegaoshop.services.crons.clear_database import clear_amount_of_purchasing

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from redis import asyncio as aioredis

from axegaoshop.settings import settings

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

        redis = aioredis.from_url(
            f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_cache_db}"
        )

        logger.info("Cache initialized")

        async_scheduler.start()

    return _startup
