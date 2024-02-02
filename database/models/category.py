from datetime import datetime

from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model
from tortoise import fields


class Category(Model):
    """таблица с категориями
    (Операционные системы, Офис, Безопасность...)"""
    id = fields.IntField(pk=True)

    created_datetime = fields.DatetimeField(default=datetime.now)

    title = fields.CharField(max_length=500)
    photo = fields.CharField(max_length=200, null=True)

    order_id = fields.IntField(null=False)

    subcategories: fields.ReverseRelation

    class Meta:
        table = "categories"
        ordering = ["order_id"]

    def subcategories_count(self) -> int:
        """
        computed subcategories count
        """
        try:
            return len(self.subcategories)
        except NoValuesFetched:
            return 0

    class PydanticMeta:
        computed = ("subcategories_count", )
        exclude = ("subcategories.products.shop_cart", )
        max_recursion = 3

    async def save(self, *args, **kwargs):
        """сохраняем и назначаем order_id"""
        last_cat_id = (await Category.all().order_by("id"))

        if not last_cat_id:
            self.order_id = 1
        else:
            self.order_id = last_cat_id[-1].order_id + 1

        await super().save(*args, **kwargs)


async def change_category_order(category_1: int, category_2: int) -> bool:
    """смена порядка в категориях"""
    category1 = await Category.get_or_none(id=category_1)
    category2 = await Category.get_or_none(id=category_2)

    if not category1 or not category2:
        return False

    cat_1_order_id_temp: int = category1.order_id

    category1.order_id = category2.order_id
    category2.order_id = cat_1_order_id_temp

    await category1.save()
    await category2.save()

    return True
