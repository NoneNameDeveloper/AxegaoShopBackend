from axegaoshop.db.models.telegram_settings import get_tg_settings, get_tg_recievers
from .service import TelegramService


async def get_telegram_data():
    telegram_settings = await get_tg_settings()

    error = False

    if not telegram_settings:
        error = True
        yield None

    recievers = await get_tg_recievers()

    if not recievers:
        error = True
        yield None

    if not error:
        a = TelegramService(telegram_settings.token, [r.telegram_id for r in recievers])
        yield a
        await a.s.close()


async def check_valid(token: str):
    """проверка на валидность введенного в админке токена"""
    tg_ = TelegramService(token, [])

    if not tg_.available():
        return False
    return True
