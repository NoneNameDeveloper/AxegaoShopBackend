from datetime import datetime

from tortoise.models import Model
from tortoise import fields

from utils.helpers import random_upper_string


class Order(Model):
    """таблица с заказами"""
    id = fields.IntField(pk=True)

    number = fields.CharField(max_length=50, unique=True, default=random_upper_string)

    promocode = fields.ForeignKeyField("axegaoshop.Promocode", related_name="orders", null=True)

    user = fields.ForeignKeyField("axegaoshop.User", related_name="orders", null=False)

    straight = fields.BooleanField(null=False, default=True)  # True - покупка напрямую, False - через корзину

    status = fields.CharField(max_length=100, default="waiting_payment")  # статус заказа (waiting_payment, canceled, finished)

    email = fields.TextField(null=False)  # почта, указанная при заполнении заявки на заказ

    payment_type = fields.CharField(max_length=100, null=False)  # выбранный способ оплаты  ("sbp", "site_balance")

    review: fields.OneToOneNullableRelation  # отзыв по этому заказу (может и не быть)
    parameters: fields.ReverseRelation["OrderParameters"]  # параметры заказа

    class Meta:
        table = "orders"

    class PydanticMeta:
        exclude = ("review", )

    async def cancel(self):
        """отменить заказ"""
        self.status = "cancelled"
        await self.save()


class OrderParameters(Model):
    """таблица с находящимися в заказе това то, но возможно то рами (версиями товара) - параметры заказа"""
    id = fields.IntField(pk=True)

    parameter = fields.ForeignKeyField("axegaoshop.Parameter", related_name="order_parameters")

    count = fields.IntField(default=1)

    order = fields.ForeignKeyField("axegaoshop.Order", related_name="order_parameters")

    class Meta:
        table = "order_parameters"
