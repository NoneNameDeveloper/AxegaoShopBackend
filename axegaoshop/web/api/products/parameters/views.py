from fastapi import APIRouter, HTTPException, Depends

from axegaoshop.db.models.product import Product, Parameter, change_parameter_order
from axegaoshop.web.api.products.parameters.schema import ParameterIn_Pydantic, ParameterCreate, ParameterUpdate, ParameterOrderChange

from axegaoshop.services.security.jwt_auth_bearer import JWTBearer
from axegaoshop.services.security.users import current_user_is_admin

router = APIRouter()


@router.get(
    path="/product/{id}/parameters",
    response_model=list[ParameterIn_Pydantic]
)
async def get_product_parameters(id: int):
    if not await Product.get_or_none(id=id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    return await ParameterIn_Pydantic.from_queryset(Parameter.filter(product_id=id))


@router.post(
    path="/product/{id}/parameters",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    response_model=ParameterIn_Pydantic
)
async def create_product_parameter(id: int, parameter: ParameterCreate):
    if not await Product.get_or_none(id=id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    parameter_ = Parameter(
        title=parameter.title,
        desctiption=parameter.description,
        price=parameter.price,
        has_sale=parameter.has_sale,
        sale_price=parameter.sale_price,
        product_id=id
    )

    await parameter_.save()

    return parameter_


@router.patch(
    path="/parameter/{id}",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    response_model=ParameterIn_Pydantic
)
async def update_product_parameter(id: int, parameter: ParameterUpdate):
    if not await Parameter.get_or_none(id=id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await Parameter.filter(id=id).update(**parameter.model_dump(exclude_unset=True))

    return await Parameter.filter(id=id).first()


@router.delete(
    path="/parameter/{id}",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    status_code=200
)
async def delete_product_parameter(id: int):
    if not await Parameter.get_or_none(id=id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await Parameter.filter(id=id).delete()


@router.post(
    "/parameter/order",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    status_code=200
)
async def change_product_order_router(param_order: ParameterOrderChange):
    res = await change_parameter_order(param_order.param_1, param_order.param_2)

    if not res:
        raise HTTPException(status_code=404, detail="NOT_FOUND")