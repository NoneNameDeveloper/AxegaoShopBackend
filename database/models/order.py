from datetime import datetime

from tortoise.models import Model
from tortoise import fields


class Order(Model):
    """таблица с заказами"""
    id = fields.IntField(pk=True)

    promocode = fields.ForeignKeyField("axegaoshop.Promocode", related_name="orders", null=True)

    user = fields.ForeignKeyField("axegaoshop.User", related_name="orders", null=False)

    status = fields.CharField(max_length=100)  # статус заказа

    email = fields.TextField()  # почта, указанная при заполнении заяви на заказ

    payment_type = fields.CharField(max_length=100)  # выбранный способ оплаты  ("sbp", "site_balance")

    is_active = fields.BooleanField(default=True)

    review: fields.OneToOneNullableRelation
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
