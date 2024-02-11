from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import UJSONResponse
from starlette.responses import JSONResponse

from axegaoshop.db.models.order import Order, OrderParameters, select_order_prices
from axegaoshop.db.models.product import Parameter
from axegaoshop.db.models.promocode import Promocode
from axegaoshop.db.models.shop_cart import ShopCart
from axegaoshop.db.models.user import User
from axegaoshop.services.payment.sbp.ozon_bank import OzoneBank
from axegaoshop.services.payment.sbp.ozon_bank_di import get_ozone_bank

from axegaoshop.web.api.orders.schema import OrderCreate, OrderIn_Pydantic, OrderStatus, OrderStatusOut, OrderFinishOut

from axegaoshop.services.security.jwt_auth_bearer import JWTBearer
from axegaoshop.services.security.users import get_current_user

router = APIRouter()


@router.post(
    "/order/",
    dependencies=[Depends(JWTBearer())],
    response_model=OrderIn_Pydantic
)
async def create_order(order_: OrderCreate, user: User = Depends(get_current_user)):
    if order_.promocode:
        promocode = await Promocode.get_or_none(name=order_.promocode)

        if not promocode or not promocode.active():
            raise HTTPException(status_code=404, detail="INVALID_PROMOCODE")

    if order_.straight:
        parameter = await Parameter.get_or_none(id=order_.parameter_id)
        if not parameter:
            raise HTTPException(status_code=404, detail="PARAMETER_NOT_FOUND")

    order = Order(
        promocode=order_.promocode,
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
        user_cart = await ShopCart.filter(user=user).all()

        if not user_cart:
            raise HTTPException(status_code=404, detail="EMPTY_SHOP_CART")

        for item in user_cart:
            order_param = OrderParameters(
                parameter_id=item.parameter_id,
                order_id=order.id,
                count=item.quantity
            )
            await order_param.save()

        await ShopCart.filter(user=user).delete()

    # установка итоговой цены на заказ
    await order.set_result_price()

    await order.refresh_from_db()

    return await OrderIn_Pydantic.from_tortoise_orm(order)


@router.get(
    "/order/{id}/check",
    dependencies=[Depends(JWTBearer())],
    response_model=OrderFinishOut,
    status_code=200
)
async def check_order(id: int, user: User = Depends(get_current_user), ozone_bank: OzoneBank = Depends(get_ozone_bank)):
    """срабатывает при нажатии кнопки "Проверить" на странице оплаты"""
    # проверка озон банка :TODO: проверка отвала озона
    if not ozone_bank:
        raise HTTPException(status_code=500, detail="Server error")

    # получение заказа по айди и принадлежности к ПОЛЬЗОВАТЕЛЮ
    order = Order.filter(user_id=user.id, id=id, status=OrderStatus.WAIT_FOR_PAYMENT)

    if not await order.exists():
        raise HTTPException(status_code=404, detail="ORDER_NOT_FOUND")

    order = await order.get()

    has_payment = await ozone_bank.has_payment(order.result_price)
    if has_payment:
        items = await order.get_items()

        return OrderFinishOut.model_validate(items)

    return UJSONResponse(status_code=200, content={"status": "waiting"})


@router.post(
    "/order/{id}/approve",
    dependencies=[Depends(JWTBearer())],
    summary="ВЫРЕЗАТЬ НА ПРОДЕ",
    status_code=200
)
async def approve_order_temp(id: int):
    order = await Order.get_or_none(id=id)

    if not order:
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await order.update_from_dict({"status": "finished"})
    await order.save()


@router.post(
    "/order/{id}/cancel",
    dependencies=[Depends(JWTBearer())],
    status_code=200
)
async def cancel_order(id: int):
    """применяется для отмены заказа по истечении срока"""
    order = await Order.get_or_none(id=id)

    if not order and not order.status == "waiting_payment":
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await order.update_from_dict({"status": "canceled"})
    await order.save()
