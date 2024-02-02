from fastapi import APIRouter, HTTPException, Depends

from database.models.product import ProductPhoto, Product
from database.models.shop_cart import add_to_cart
from database.models.user import User
from schemas.products import PhotoIn_Pydantic, PhotoCreate, PhotoUpdate, ProductToCart
from schemas.users import UserIn_Pydantic, UserCart_Pydantic
from security.auth_bearer import JWTBearer
from utils.users_misc import current_user_is_admin, get_current_user

router = APIRouter(tags=["Shop Cart"])


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
    if not await Product.get_or_none(id=data.product_id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await add_to_cart(user.id, data.product_id, data.parameter_id, data.count)

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
