from decimal import Decimal

from tortoise.models import Model
from tortoise import fields

from axegaoshop.services.utils import random_string


def random_upper_string():
    return random_string(8).upper()

class Order(Model):
    """таблица с заказами"""
    id = fields.IntField(pk=True)

    number = fields.CharField(max_length=50, unique=True, default=random_upper_string)

    promocode = fields.ForeignKeyField("axegaoshop.Promocode", related_name="orders", null=True)

    user = fields.ForeignKeyField("axegaoshop.User", related_name="orders", null=False)

    straight = fields.BooleanField(null=False, default=True)  # True - покупка напрямую, False - через корзину

    result_price = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    status = fields.CharField(max_length=100,
                              default="waiting_payment")  # статус заказа (waiting_payment, canceled, finished)

    email = fields.TextField(null=False)  # почта, указанная при заполнении заявки на заказ

    payment_type = fields.CharField(max_length=100, null=False)  # выбранный способ оплаты  ("sbp", "site_balance")

    review: fields.OneToOneNullableRelation  # отзыв по этому заказу (может и не быть)
    parameters: fields.ReverseRelation["OrderParameters"]  # параметры заказа

    class Meta:
        table = "orders"

    class PydanticMeta:
        exclude = ("review",)

    async def cancel(self):
        """отменить заказ"""
        self.status = "cancelled"
        await self.save()

    async def set_result_price(self) -> Decimal:
        """установить итоговую цену исходя из всех товаров / количества одного товара"""
        result_price = 0
        await self.fetch_related('order_parameters')
        if self.straight:

            result_price = await (await self.order_parameters[0].parameter).get_price() * self.order_parameters[0].count

        else:
            for parameter in self.order_parameters:
                result_price += (await parameter).get_price() * parameter.count

        if self.promocode:
            result_price = result_price - (result_price * Decimal.from_float((await self.promocode).sale_percent / 100))

        self.result_price = result_price
        await self.save()


class OrderParameters(Model):
    """таблица с находящимися в заказе това то, но возможно то рами (версиями товара) - параметры заказа"""
    id = fields.IntField(pk=True)

    parameter = fields.ForeignKeyField("axegaoshop.Parameter", related_name="order_parameters")

    count = fields.IntField(default=1)

    order = fields.ForeignKeyField("axegaoshop.Order", related_name="order_parameters")

    class Meta:
        table = "order_parameters"
