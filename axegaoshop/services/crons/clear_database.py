import datetime
from datetime import timedelta

from axegaoshop.db.models.order import Order
from axegaoshop.db.models.replenish import Replenish
from axegaoshop.services.cache.redis_service import rem_amount

from axegaoshop.logging import logger


async def clear_amount_of_purchasing() -> None:
    """завершение заказов и заявок на пополнения для освобождения
    суммы с копейками"""
    ten_minutes_delta = datetime.datetime.now() - timedelta(minutes=10)
    orders = Order.filter(
        created_datetime__lt=ten_minutes_delta, status="waiting_payment"
    )
    replenishes = Replenish.filter(
        created_datetime__lt=ten_minutes_delta, status="waiting_payment"
    )

    await orders.update(status="canceled")
    await orders.update(status="canceled")

    order_amounts = await orders.values_list("result_price")
    replenish_amounts = await replenishes.values_list("result_price")

    total = order_amounts + replenish_amounts

    pruned_count: int = 0

    for value in total:
        if len(value) != 0 and value[0]:
            pruned_count += 1
            await rem_amount(float(value[0]))

    if pruned_count != 0:
        logger.success(f"Pruned orders successfully: {pruned_count}")
