from fastapi import APIRouter, HTTPException, Depends

from axegaoshop.db.models.order import Order
from axegaoshop.db.models.product import Product
from axegaoshop.db.models.shop_cart import add_to_cart
from axegaoshop.db.models.user import User

from axegaoshop.web.api.products.schema import ProductToCart
from axegaoshop.web.api.users.schema import UserCart_Pydantic

from axegaoshop.services.security.jwt_auth_bearer import JWTBearer
from axegaoshop.services.security.users import get_current_user


router = APIRouter()


@router.post(
    path="/cart/add",
    dependencies=[Depends(JWTBearer())],
    response_model=UserCart_Pydantic,
    description="""
Работа с корзиной пользователя
1. В count указывать **полное** количество товара (не инкремент/декремент).
2. При передаче count=0 происходит **удаление товара** из корзины.
"""
)
async def add_or_create_cart(data: ProductToCart, user: User = Depends(get_current_user)):
    if not await Product.get_or_none(id=data.product_id, parameters__id=data.parameter_id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await add_to_cart(user.id, data.product_id, data.parameter_id, data.count)

    order = await Order.get_or_none(user=user, status="waiting_payment")
    # отменяем заказ, если есть активный
    if order:
        await order.cancel()

    return await UserCart_Pydantic.from_queryset_single(User.filter(id=user.id).first())

# @router.patch(
#     path="/photo/{id}",
#     dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
#     response_model=PhotoIn_Pydantic
# )
# async def update_product_photo(id: int, parameter: PhotoUpdate):
#     if not await ProductPhoto.get_or_none(id=id):
#         raise HTTPException(status_code=404, detail="NOT_FOUND")
#
#     await ProductPhoto.filter(id=id).update(**parameter.model_dump(exclude_unset=True))
#
#     return await ProductPhoto.filter(id=id).first()
#
#
# @router.delete(
#     path="/photo/{id}",
#     dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
#     status_code=200
# )
# async def delete_product_photo(id: int):
#     if not await ProductPhoto.get_or_none(id=id):
#         raise HTTPException(status_code=404, detail="NOT_FOUND")
#
#     await ProductPhoto.filter(id=id).delete()
