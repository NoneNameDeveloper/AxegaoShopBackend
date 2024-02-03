import typing

from pydantic import BaseModel, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo
from tortoise.contrib.pydantic import pydantic_model_creator

from database.models.order import Order, OrderParameters

from schemas.payment_types import PaymentTypesList


class OrderCreate(BaseModel):
    promocode: typing.Optional[str] = None
    straight: bool
    email: str
    payment_type: str

    parameter_id: int | None = None
    count: int | None = None

    @field_validator("payment_type")
    @classmethod
    def validate_payment_type(cls, v: str) -> str:
        if v not in PaymentTypesList:
            raise ValueError("Unsupported payment type")
        return v

    @field_validator("count")
    @classmethod
    def validate_count(cls, v: int | None) -> int | None:
        if v is not None:
            if v <= 0:
                raise ValueError("invalid count")
        return v

    @model_validator(mode="after")
    def validate_order_params(self) -> "OrderCreate":
        if self.straight:
            if not self.parameter_id or not self.count:
                raise ValueError("parameter_id or count required for straight payment")

        if not self.straight:
            if self.parameter_id or self.count:
                raise ValueError("parameter_id or count shouldn't be used in non-straight payment!")

        return self


OrderIn_Pydantic = pydantic_model_creator(Order, exclude=("user.shop_cart", "reviews"))
