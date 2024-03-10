from datetime import datetime

from tortoise.models import Model
from tortoise import fields

from axegaoshop.db.models.order import OrderParameters
from axegaoshop.db.models.review import Review
from axegaoshop.services.image.avatar import create_user_photo


class User(Model):
    id = fields.IntField(pk=True)

    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255, null=True)
    email = fields.CharField(max_length=255, null=True)

    balance = fields.DecimalField(max_digits=10, decimal_places=2, default=0)

    photo = fields.CharField(max_length=255)

    reg_datetime = fields.DatetimeField(default=datetime.now)

    is_active = fields.BooleanField(default=True)
    is_anonymous = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)

    reviews: fields.ReverseRelation
    orders: fields.ReverseRelation
    shop_cart: fields.ForeignKeyRelation
    tickets: fields.ReverseRelation

    class Meta:
        table = "users"

    class PydanticMeta:
        exclude = ("password", "reviews", "tickets")

    def __str__(self):
        return self.username

    async def save(self, *args, **kwargs):
        """генерация и добавление аватарки к пользователю (символьная)"""
        if not self.photo:
            self.photo = create_user_photo(self.username)  # передаем login в create_user_photo
        await super().save(*args, **kwargs)

    async def add_balance(self, amount: float):
        """добавление баланса к текущему"""
        self.balance += amount
        await self.save()

    async def clear_shop_cart(self):
        """очищение корзины пользователя"""
        await self.shop_cart.all().delete()

    async def get_available_products_to_comment(self):
        """получение товаров (завершенные заказы), по которым не было оставлено комментариев"""

        # Get the product IDs for which the user has not written a review yet
        reviewed_products = await Review.filter(user=self).values_list('product_id', 'order_id')

        # Get the product IDs and order IDs from the user's orders
        order_products = await OrderParameters.filter(order__user=self, order__status="finished").values_list('parameter__product__id', 'parameter__product__title', 'order_id')

        # Find the products that are in the user's orders but have not been reviewed
        # Use a set to keep track of unique combinations of product_id and order_id
        unique_combinations = set()

        # Find the products that are in the user's orders but have not been reviewed
        available_products = [
            [product_id, title, order_id]
            for product_id, title, order_id in order_products
            if (product_id, order_id) not in reviewed_products and (product_id, order_id) not in unique_combinations and not unique_combinations.add((product_id, order_id))
        ]

        return available_products
