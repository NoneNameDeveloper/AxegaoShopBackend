from tortoise.models import Model
from tortoise import fields


class Payment(Model):
    """таблица с данными об оплате"""

    id = fields.IntField(pk=True)
