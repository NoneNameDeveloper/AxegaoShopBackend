from tortoise.fields import ReverseRelation
from tortoise.models import Model
from tortoise import fields


class Promocode(Model):
    """таблица с промокодами"""
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=100, unique=True)
    activations_count = fields.IntField(default=1)
    sale_percent = fields.FloatField()

    created_datetime = fields.DatetimeField(auto_now_add=True)

    orders: ReverseRelation

    class Meta:
        table = "promocodes"

    # class PydanticMeta:
    #     ...
    #     # exclude = ("orders", "created_datetime")

    async def use(self):
        """используем промокод"""
        self.activations_count -= 1
        await self.save()

    async def active(self):
        """проверка на активность промокода"""
        return self.activations_count == -1 or self.activations_count > 0
