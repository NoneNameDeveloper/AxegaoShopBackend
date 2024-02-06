import typing

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from axegaoshop.db.models.category import Category


class CategoryCreate(BaseModel):
    title: str
    photo: str


class CategoryOrderChange(BaseModel):
    category_1: int
    category_2: int


class CategoryUpdate(BaseModel):
    title: typing.Optional[str] = None
    photo: typing.Optional[str] = None


CategoryIn_Pydantic = pydantic_model_creator(Category)
