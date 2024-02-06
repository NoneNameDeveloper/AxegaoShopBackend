import typing
from decimal import Decimal

from pydantic import BaseModel

from datetime import datetime

from tortoise.contrib.pydantic import pydantic_model_creator

from axegaoshop.db.models.user import User


class UserCreate(BaseModel):
    username: str
    password: typing.Optional[str] = None
    email: typing.Optional[str] = None


class UserUpdate(BaseModel):
    username: typing.Optional[str] = None
    photo: typing.Optional[str] = None


class UserUpdateAdmin(UserUpdate):
    is_admin: typing.Optional[bool] = None


class UserOutput(BaseModel):
    username: str
    email: typing.Optional[str]
    photo: typing.Optional[str]
    is_admin: bool
    balance: Decimal
    reg_datetime: datetime
    is_anonymous: bool

    class Config:
        from_attributes = True


UserIn_Pydantic = pydantic_model_creator(User, exclude=("is_admin", "shop_cart.id", "shop_cart.items.id", "shop_cart.cart_product"))

UserForAdmin_Pydantic = pydantic_model_creator(User, exclude=("shop_cart", "orders", "reviews"))

UserCart_Pydantic = pydantic_model_creator(
    User,
    exclude=(
        "shop_cart.id", "shop_cart.product.options", "shop_cart.product.category", "shop_cart.product.id",
        "shop_cart.product.parameters", "shop_cart.parameter.data", "shop_cart.parameter.id"
        "shop_cart.product.category_id", "shop_cart.product.product_photos.id",
        "shop_cart.parameter.product", "shop_cart.reviews", "orders"
    )
)
