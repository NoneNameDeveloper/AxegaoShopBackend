from fastapi import APIRouter, Depends, HTTPException

from utils.users_misc import get_current_user
from database.models.order import Order, OrderParameters
from database.models.product import Parameter
from database.models.promocode import Promocode
from database.models.shop_cart import ShopCart
from database.models.user import User
from schemas.orders import OrderCreate, OrderIn_Pydantic
from security.auth_bearer import JWTBearer



router = APIRouter(tags=["Order"])


@router.post(
    "/order/",
    dependencies=[Depends(JWTBearer())],
    response_model=OrderIn_Pydantic
)
async def create_order(order_: OrderCreate, user: User = Depends(get_current_user)):
    if order_.promocode:
        promocode = await Promocode.get_or_none(name=order_.promocode)

        if not promocode or not await promocode.active():
            raise HTTPException(status_code=404, detail="INVALID_PROMOCODE")
        order_.promocode = promocode.id

    parameter = await Parameter.get_or_none(id=order_.parameter_id)
    if not parameter:
        raise HTTPException(status_code=404, detail="PARAMETER_NOT_FOUND")

    order = Order(
        promocode_id=order_.promocode,
        user_id=user.id,
        straight=order_.straight,
        payment_type=order_.payment_type,
        email=order_.email
    )
    await order.save()

    if order_.straight:
        order_params = OrderParameters(
            order_id=order.id,
            parameter_id=order_.parameter_id,
            count=order_.count
        )
        await order_params.save()

    else:
        user_cart = await ShopCart.filter(user_id=user.id).all()

        if not user_cart:
            raise HTTPException(status_code=404, detail="EMPTY_SHOP_CART")

        for item in user_cart:
            order_param = OrderParameters(
                parameter_id=item.parameter_id,
                order_id=order.id,
                count=item.quantity
            )
            await order_param.save()

        await ShopCart.filter(user_id=user.id).delete()

    await order.set_result_price()

    await order.refresh_from_db()

    return await OrderIn_Pydantic.from_tortoise_orm(order)



