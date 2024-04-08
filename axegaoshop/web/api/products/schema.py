import typing

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from axegaoshop.db.models.product import Product

from axegaoshop.web.api.products.options.schema import OptionCreate
from axegaoshop.web.api.products.parameters.schema import ParameterCreate


class ProductSorting(BaseModel):
    price: typing.Optional[bool] = False  # сортировка по цене (false - возрастание)
    rating: typing.Optional[bool] = False  # сортировка по рейтингу (false - возрастание)
    sale: typing.Optional[bool] = False  # сортировка по скидке (false - все товары, true - только со скидками)


class ProductCreate(BaseModel):
    title: str
    description: str
    card_price: float
    subcategory_id: int
    parameters: list[ParameterCreate]
    options: typing.Optional[list[OptionCreate]] = None
    photos: typing.Optional[list[str]] = []

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "title": "Windows 11",
    #                 "description": "Ключи для активации Windows 11",
    #                 "card_price": 4000,
    #                 "give_type": "string",
    #                 "subcategory_id": 1,
    #                 "parameters": [
    #                     {
    #                         "title": "Windows 11 Professional",
    #                         "price": 4500,
    #                         "has_sale": False,
    #                         "data": [
    #                                 "FWBFIWEF-FWEF-W-EFWE-F-WE", "QWEQE-QEQWEQW-EQWEQWEQW-GERGRE"
    #                         ]
    #                     },
    #                     {
    #                         "title": "Windows 11 Home",
    #                         "price": 4300,
    #                         "has_sale": True,
    #                         "sale_price": 4000,
    #                         "data": [
    #                                 "FWBFIWEF-FWEF-W-EFWE-F-WE", "QWEQE-QEQWEQW-EQWEQWEQW-GERGRE"
    #                         ]
    #                     }
    #                 ],
    #                 "options": [
    #                     {
    #                         "title": "Тип поставки",
    #                         "value": "Ключ"
    #                     },
    #                     {
    #                         "title": "Код",
    #                         "value": "100",
    #                         "is_pk": True
    #                     }
    #                 ],
    #                 "photos": [
    #
    #                         "photo": "grfwefwrgre.jpg",
    #
    #                         "photo": "qlmzvywrge.jpg",
    #                 ]
    #             }
    #         ]
    #     }
    # }


class ProductOrderChange(BaseModel):
    product_1: int
    product_2: int


class ProductToCart(BaseModel):
    product_id: int
    parameter_id: int
    count: typing.Optional[int] = 1


class ProductUpdate(BaseModel):
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    card_price: typing.Optional[float] = None
    subcategory_id: typing.Optional[int] = None


class ProductDataOut(BaseModel):
    parameter_id: int
    items: list[str]


ProductIn_Pydantic = pydantic_model_creator(
    Product,
    exclude=(
        "parameters.data.id", "parameters.cart_product",
        "cart_product", "product_photos.id"
    ))
