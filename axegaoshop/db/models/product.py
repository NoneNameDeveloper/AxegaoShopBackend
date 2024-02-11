from datetime import datetime

from tortoise.expressions import Q
from tortoise.models import Model
from tortoise import fields


class Product(Model):
    """таблица с товарами (винда 11, винда 10...)"""
    id = fields.IntField(pk=True)

    created_datetime = fields.DatetimeField(default=datetime.now)

    title = fields.CharField(max_length=500, null=False)
    description = fields.TextField()

    card_price = fields.DecimalField(max_digits=10, decimal_places=2)  # цена на карточке из первой версии товара
    card_has_sale = fields.BooleanField(default=False)  # скидка из первой версии товара
    card_sale_price = fields.DecimalField(max_digits=10, decimal_places=2)  # скидка из первой версии товара

    subcategory: fields.ForeignKeyRelation = fields.ForeignKeyField("axegaoshop.Subcategory",
                                                                    related_name="products")

    give_type = fields.CharField(max_length=30, null=False, default="string")  # string/file - тип выдачи товара

    order_id = fields.BigIntField(null=False)

    parameters: fields.ReverseRelation["Parameter"]
    photos: fields.ReverseRelation["ProductPhoto"]
    options: fields.ReverseRelation["Option"]
    shop_cart: fields.ReverseRelation

    def sale_percent(self) -> int:
        """процент скидки (высчитывается автоматом в пидантик модель)"""

        return int((self.card_sale_price * 100) / self.card_price)

    class PydanticMeta:
        exclude = ("subcategory", "shop_cart", "created_datetime")
        computed = ["sale_percent", ]

    class Meta:
        table = "products"
        ordering = ["order_id"]

    async def save(self, *args, **kwargs):
        """сохраняем и назначаем order_id"""
        last_product_id = (await Product.filter(subcategory_id=self.subcategory_id).order_by("id"))

        if not last_product_id:
            self.order_id = 1
        else:
            self.order_id = last_product_id[-1].order_id + 1

        await super().save(*args, **kwargs)


class Parameter(Model):
    """таблица с параметрами - версиями товара (винда домашняя, винда профессиональная...)"""
    id = fields.IntField(pk=True)

    title = fields.TextField(null=False)

    price = fields.DecimalField(max_digits=10, decimal_places=2, null=False)

    has_sale = fields.BooleanField(default=False)
    sale_price = fields.DecimalField(max_digits=10, decimal_places=2)

    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField("axegaoshop.Product",
                                                                         related_name="parameters")
    order_id = fields.IntField(null=False)

    shop_cart: fields.ReverseRelation
    data: fields.ReverseRelation["ProductData"]
    order_parameters: fields.ReverseRelation

    class Meta:
        table = "parameters"
        ordering = ["order_id"]

    class PydanticMeta:
        exclude = ["shop_cart", "product", "data", "order_parameters", "reviews"]

    async def save(self, *args, **kwargs):
        """сохраняем и назначаем order_id"""
        last_param_id = (await Parameter.filter(product_id=self.product_id).order_by("id"))

        if not last_param_id:
            self.order_id = 1
        else:
            self.order_id = last_param_id[-1].order_id + 1

        await super().save(*args, **kwargs)

    async def get_price(self):
        """get result price for one parameter"""
        if self.has_sale:
            return self.sale_price
        else:
            return self.price


class ProductData(Model):
    """таблица с самими товарами (ключами..)"""
    id = fields.IntField(pk=True)

    parameter: fields.ForeignKeyRelation["Parameter"] = fields.ForeignKeyField(
        "axegaoshop.Parameter", related_name="data"
    )

    value = fields.TextField(null=False)

    is_active = fields.BooleanField(default=True, null=False)

    class PydanticMeta:
        exclude = ("parameer",)

    class Meta:
        table = "product_data"


class Option(Model):
    """таблица с характеристиками (код, метод установки...)"""
    id = fields.IntField(pk=True)

    title = fields.TextField(null=False)

    value = fields.TextField(null=False)

    is_pk = fields.BooleanField(default=False)

    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField("axegaoshop.Product", related_name="options")

    class Meta:
        table = "options"

    class PydanticMeta:
        exclude = ("product",)

    async def save(self, *args, **kwargs):
        """сохраняем, но перед этим
        проверяем, если такой параметр же где то стоит (код товара),
        возвращаем ошибку"""
        # if self.is_pk:
        #     if await Option.get_or_none(value=self.value):
        #         return "ALREADY_HAVE"

        await super().save(*args, **kwargs)

    async def is_available(self) -> bool:
        if self.is_pk:
            query = await Option.filter(Q(title=self.title) & Q(value=self.value))

            if query:
                return False
        return True


class ProductPhoto(Model):
    """фотографии к товарам"""
    id = fields.IntField(pk=True)

    photo = fields.CharField(max_length=200)

    main = fields.BooleanField(default=False)

    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField(
        "axegaoshop.Product",
        related_name="product_photos"
    )

    class Meta:
        table = "product_photos"
        ordering = ["-main"]

    class PydanticMeta:
        exclude = ("product",)


async def change_product_order(product_1: int, product_2: int) -> bool:
    """смена порядка в товарах"""
    product1 = await Product.get_or_none(id=product_1)
    product2 = await Product.get_or_none(id=product_2)

    if not product1 or not product2:
        return False

    product_1_order_id_temp: int = product1.order_id

    product1.order_id = product2.order_id
    product2.order_id = product_1_order_id_temp

    await product1.save()
    await product2.save()

    return True


async def change_parameter_order(parameter_1: int, parameter_2: int) -> bool:
    """смена порядка в параметрах (версиях товара)"""
    parameter1 = await Product.get_or_none(id=parameter_1)
    parameter2 = await Product.get_or_none(id=parameter_2)

    if not parameter2 or not parameter1:
        return False

    param_1_order_id_temp: int = parameter1.order_id

    parameter1.order_id = parameter2.order_id
    parameter2.order_id = param_1_order_id_temp

    await parameter1.save()
    await parameter2.save()

    return True


async def get_items_data_for_order(parameter_id: int, count: int) -> list[ProductData]:
    """получение данных по товару из заказа и удаление этих ключей из базы данных (архивирование)"""
    items = await ProductData.filter(parameter__id=parameter_id, is_active=True).limit(count)

    for item in items:
        await item.update_from_dict({"is_active": False})

    return items
