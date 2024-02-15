import typing

from pydantic import BaseModel, model_validator
from tortoise.contrib.pydantic import pydantic_model_creator

from axegaoshop.db.models.product import Parameter

#
# class ParameterDataCreate(BaseModel):
#     value: str


class ParameterCreate(BaseModel):
    title: str
    price: float
    has_sale: bool = False
    sale_price: float = 0.0
    data: typing.Optional[list[str]] = []

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


class ParameterUpdate(BaseModel):
    title: str
    price: float
    has_sale: bool = False
    sale_price: float = 0.0


class ParameterOrderChange(BaseModel):
    param_1: int
    param_2: int


ParameterIn_Pydantic = pydantic_model_creator(Parameter, exclude=("product", ))