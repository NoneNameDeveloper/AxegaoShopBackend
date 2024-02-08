from datetime import datetime

from tortoise.models import Model
from tortoise import fields

from axegaoshop.db.models.order import OrderParameters
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

    class Meta:
        table = "users"

    class PydanticMeta:
        exclude = ("password", "reviews")

    def __str__(self):
        return self.username

    async def save(self, *args, **kwargs):
        """генерация и добавление аватарки к пользователю (символьная)"""
        if not self.photo:
            self.photo = create_user_photo(self.username)  # передаем login в create_user_photo
        await super().save(*args, **kwargs)

    async def get_available_products_to_comment(self) -> list[list[str, str]]:
        """получение товаров (завершенные заказы), по которым не было оставлено комментариев"""

        query = (
            OrderParameters.filter(order__user_id=self.id, order__status="finished", order__review__isnull=True)
            .distinct()
            .values_list('parameter__product__id', 'parameter__product__title', 'order__id')
        )

        return await query
