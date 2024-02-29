import asyncio
from decimal import Decimal
from typing import Any

from tortoise.models import Model
from tortoise import fields

from axegaoshop.db.models.product import Parameter, get_items_data_for_order
from axegaoshop.db.models.review import Review
from axegaoshop.services.cache.redis_service import rem_amount
from axegaoshop.services.utils import random_upper_string, generate_unique_sum_postfix


class Order(Model):
    """таблица с заказами"""
    id = fields.IntField(pk=True)

    number = fields.CharField(max_length=50, unique=True, default=random_upper_string)

    promocode = fields.ForeignKeyField("axegaoshop.Promocode", related_name="orders", null=True)

    user = fields.ForeignKeyField("axegaoshop.User", related_name="orders", null=False)

    straight = fields.BooleanField(null=False, default=True)  # True - покупка напрямую, False - через корзину

    result_price = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    created_datetime = fields.DatetimeField(auto_now_add=True)

    status = fields.CharField(max_length=100,
                              default="waiting_payment")  # статус заказа (waiting_payment, canceled, finished)

    email = fields.TextField(null=False)  # почта, указанная при заполнении заявки на заказ

    payment_type = fields.CharField(max_length=100, null=False)  # выбранный способ оплаты  ("sbp", "site_balance")
    # отзывы по этому заказу (может и не быть, может быть максимум
    # столько, сколько в заказе товаров)
    reviews: fields.ForeignKeyNullableRelation
    order_parameters: fields.ReverseRelation["OrderParameters"]  # параметры заказа
    payment: fields.OneToOneRelation

    class Meta:
        table = "orders"

    class PydanticMeta:
        exclude = ("reviews",)

    async def cancel(self):
        """отменить заказ"""
        self.status = "canceled"
        await self.save()

    async def set_result_price(self):
        """установить итоговую цену исходя из всех товаров / количества одного товара"""
        result_price = 0
        await self.fetch_related('order_parameters')
        if self.straight:

            result_price = await (await self.order_parameters[0].parameter).get_price() * self.order_parameters[0].count

        else:
            for parameter in self.order_parameters:
                result_price += await (await parameter.parameter).get_price() * parameter.count

        if self.promocode:
            result_price = result_price - (result_price * Decimal.from_float((await self.promocode).sale_percent / 100))

        price_postfix: float = await generate_unique_sum_postfix()

        self.result_price = float(result_price) + float(price_postfix)

        await self.save()

    async def review_available(self, product_id: int) -> bool:
        """проверка, доступен ли отзыв на этот товар из заказа"""
        existing_reviews = await Review.filter(order=self, product_id=product_id).count()
        if existing_reviews > 0:
            return False  # Отзыв уже существует для одного из товаров в заказе

        return True  # Нет отзывов для всех товаров в заказе

    async def get_order_products(self) -> set[Any]:
        """получение всех товаров (не версий) из заказа"""
        order_products = set()

        await self.fetch_related('order_parameters')

        for o_p in self.order_parameters:
            order_products.add((await (await o_p.parameter.first()).product).id)

        return order_products

    async def get_items(self) -> dict:
        """получение товаров из заказа"""
        # получение всей инфы на итоговую страницу, кроме самих товаров
        order_data = await Parameter.filter(order_parameters__order=self).values_list(
            'title',  # название версии товара
            'id',  # айди параметра
            'order_parameters__count',  # количество товаров в заказе
            'order_parameters__order__number',  # номер заказа
            'order_parameters__order__id',  # айди заказа
            'order_parameters__order__result_price',  # итоговая цена в заказе
            'give_type'  # тип выдачи
        )

        items_dict = {}

        [items_dict.setdefault(
            data[0], await get_items_data_for_order(data[1], data[2])) for data in order_data]

        result_dict = {
            "id": order_data[0][4],
            "number": order_data[0][3],
            "total_price": order_data[0][5],
            "order_data": [
                {
                    "id": res_data[1],
                    "title": res_data[0],
                    "count": res_data[2],
                    "give_type": order_data[0][6],
                    "items": [item.value for item in items_dict[res_data[0]]]

                } for res_data in order_data
            ]
        }

        return result_dict

    async def finish(self):
        """завершение заказа, выдача товара"""
        self.status = 'finished'
        await rem_amount(float(self.result_price))
        await self.save()


class OrderParameters(Model):
    """таблица с находящимися в заказе това то, но возможно то рами (версиями товара) - параметры заказа"""
    id = fields.IntField(pk=True)

    parameter = fields.ForeignKeyField("axegaoshop.Parameter", related_name="order_parameters")

    count = fields.IntField(default=1)

    order = fields.ForeignKeyField("axegaoshop.Order", related_name="order_parameters")

    class Meta:
        table = "order_parameters"
