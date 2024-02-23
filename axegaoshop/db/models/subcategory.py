from datetime import datetime

from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model
from tortoise import fields


class Subcategory(Model):
    """таблица с подкатегориями
    (Операционные системы -> *Windows*, *Linux*...)"""
    id = fields.IntField(pk=True)

    created_datetime = fields.DatetimeField(default=datetime.now)

    title = fields.CharField(max_length=500)

    category: fields.ForeignKeyRelation = fields.ForeignKeyField("axegaoshop.Category",
                                                                 related_name="subcategories")

    order_id = fields.IntField(null=False)

    products: fields.ReverseRelation

    class Meta:
        table = "subcategories"
        ordering = ["order_id"]

    def product_count(self) -> int:
        """получение количество товаров в подкатегории"""
        try:
            return len(self.products)
        except NoValuesFetched:
            return 0

    class PydanticMeta:
        computed = ("product_count",)
        allow_cycles = True
        max_recursion = 3

    async def save(self, *args, **kwargs):
        """сохраняем и назначаем order_id"""
        if not kwargs.get("repeat"):
            last_cat_id = (await Subcategory.filter(category_id=self.category_id).order_by("id"))
            if not last_cat_id:
                self.order_id = 1
            else:
                self.order_id = last_cat_id[-1].id + 1

        await super().save(*args, **kwargs)


async def change_subcategory_order(subcategory_1: int, subcategory_2: int) -> bool:
    """смена порядка в подкатегориях"""
    subcategory1 = await Subcategory.get_or_none(id=subcategory_1)
    subcategory2 = await Subcategory.get_or_none(id=subcategory_2)

    if not subcategory1 or not subcategory2:
        return False

    subcategory1_order_id_temp: int = subcategory1.order_id

    subcategory1.order_id = subcategory2.order_id
    subcategory2.order_id = subcategory1_order_id_temp

    await subcategory1.save(repeat=True)
    await subcategory2.save(repeat=True)

    return True