import typing

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from axegaoshop.db.models.order import Order
from axegaoshop.db.models.review import Review


class ReviewPhotoCreate(BaseModel):
    """фотографии к отзыву"""
    photo: str


class ReviewCreate(BaseModel):
    """тело отзыва"""
    rate: int
    text: str
    images: typing.Optional[list[ReviewPhotoCreate]] = None
    order_id: int


class ReviewOutput(BaseModel):
    """отзыв на страницы пользователям"""
    rate: int
    text: str
    images: typing.Optional[list[str]] = None

    class Config:
        from_attributes = True


class ReviewUpdate(BaseModel):
    """обновление отзыва (пока только текст)"""
    text: str


ReviewIn_Pydantic = pydantic_model_creator(Order, exclude=("user", "straight", "result_price", "status", ))
ReviewInAdmin_Pydantic = pydantic_model_creator(Review, exclude=("order", "user.orders", "user.shop_cart"))
