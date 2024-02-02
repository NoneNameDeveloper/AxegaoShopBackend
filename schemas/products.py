import datetime
import typing

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from database.models.product import Product, Option, Parameter, ProductPhoto


class ParameterDataCreate(BaseModel):
    value: str


class ProductSorting(BaseModel):
    price: typing.Optional[bool] = False  # сортировка по цене (false - возрастание)
    rating: typing.Optional[bool] = False  # сортировка по рейтингу (false - возрастание)
    sale: typing.Optional[bool] = False  # сортировка по скидке (false - все товары, true - только со скидками)


class ParameterCreate(BaseModel):
    title: str
    price: float
    has_sale: bool = False
    sale_price: float = 0.0
    data: list[ParameterDataCreate]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Windows 11 Professional",
                    "price": 4500,
                    "has_sale": False,
                    "data": [
                        {
                            "value": "FWBFIWEF-FWEF-W-EFWE-F-WE"
                        },
                        {
                            "value": "QWEQE-QEQWEQW-EQWEQWEQW-GERGRE"
                        }
                    ]
                }
            ]
        }
    }


class OptionCreate(BaseModel):
    title: str
    value: str
    is_pk: typing.Optional[bool] = False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Тип поставки",
                    "value": "Ключ"
                },
                {
                    "title": "Код",
                    "value": "100",
                    "is_pk": True
                }
            ]
        }
    }


class PhotoCreate(BaseModel):
    photo: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "photo": "grfwefwrgre.jpg",
                },
                {
                    "photo": "qlmzvywrge.jpg",
                }
            ]
        }
    }


class ProductId(BaseModel):
    id: int

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    title: str
    description: str
    card_price: float
    subcategory_id: int
    give_type: typing.Optional[str] = "string"
    parameters: list[ParameterCreate]
    options: typing.Optional[list[OptionCreate]] = None
    photos: typing.Optional[list[PhotoCreate]]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Windows 11",
                    "description": "Ключи для активации Windows 11",
                    "card_price": 4000,
                    "give_type": "string",
                    "subcategory_id": 1,
                    "parameters": [
                        {
                            "title": "Windows 11 Professional",
                            "price": 4500,
                            "has_sale": False,
                            "data": [
                                {
                                    "value": "FWBFIWEF-FWEF-W-EFWE-F-WE"
                                },
                                {
                                    "value": "QWEQE-QEQWEQW-EQWEQWEQW-GERGRE"
                                }
                            ]
                        },
                        {
                            "title": "Windows 11 Home",
                            "price": 4300,
                            "has_sale": True,
                            "sale_price": 4000,
                            "data": [
                                {
                                    "value": "FWBFIWEF-FWEF-W-EFWE-F-WE"
                                },
                                {
                                    "value": "QWEQE-QEQWEQW-EQWEQWEQW-GERGRE"
                                }
                            ]
                        }
                    ],
                    "options": [
                        {
                            "title": "Тип поставки",
                            "value": "Ключ"
                        },
                        {
                            "title": "Код",
                            "value": "100",
                            "is_pk": True
                        }
                    ],
                    "photos": [
                        {
                            "photo": "grfwefwrgre.jpg",
                        },
                        {
                            "photo": "qlmzvywrge.jpg",
                        }
                    ]
                }
            ]
        }
    }


class CategoryInDB(BaseModel):
    created_datetime: datetime.datetime
    title: str
    photo: str


class CategoryGet(BaseModel):
    title: str
    photo: str


class OptionUpdate(BaseModel):
    title: typing.Optional[str]
    value: typing.Optional[str]
    is_pk: typing.Optional[bool]


class ParameterUpdate(BaseModel):
    title: str
    price: float
    has_sale: bool = False
    sale_price: float = 0.0



class ParameterOrderChange(BaseModel):
    param_1: int
    param_2: int


class PhotoUpdate(BaseModel):
    photo: str
    main: typing.Optional[bool] = False


class ProductOrderChange(BaseModel):
    product_1: int
    product_2: int


class ProductToCart(BaseModel):
    product_id: int
    parameter_id: int
    count: typing.Optional[int] = 1


ProductIn_Pydantic = pydantic_model_creator(
    Product,
    exclude=(
        "parameters.data.id", "parameters.cart_product",
        "cart_product", "product_photos.id"
    ))

OptionIn_Pydantic = pydantic_model_creator(Option, exclude=("product", ))
ParameterIn_Pydantic = pydantic_model_creator(Parameter, exclude=("product", ))
PhotoIn_Pydantic = pydantic_model_creator(ProductPhoto, exclude=("product", ))
