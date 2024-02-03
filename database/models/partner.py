from tortoise.models import Model
from tortoise import fields


class Partners(Model):
    """таблица с партнерами"""
    id = fields.IntField(pk=True)

    created_datetime = fields.DatetimeField(auto_now_add=True)

    photo = fields.CharField(max_length=100)

    class Meta:
        table = "partners"

    class PydanticMeta:
        exclude = ("created_datetime", )
