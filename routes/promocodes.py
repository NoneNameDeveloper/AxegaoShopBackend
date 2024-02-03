from fastapi import APIRouter, HTTPException, Depends

from database.models.promocode import Promocode

from schemas.promocodes import PromocodeIn_Pydantic, CreatePromocode, UpdatePromocode
from security.auth_bearer import JWTBearer
from utils.users_misc import current_user_is_admin

router = APIRouter(tags=["Promocodes"])


@router.get(
    path="/promocodes",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    response_model=list[PromocodeIn_Pydantic]
)
async def get_promocodes(limit: int = 0, offset: int = 20):
    return await PromocodeIn_Pydantic.from_queryset(Promocode.all().limit(limit).offset(offset))


@router.post(
    path="/promocodes/",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    status_code=201
)
async def create_promocode(promocode: CreatePromocode):
    """Для создания безлимитного промо: *activations_count = -1*"""
    await Promocode.create(**promocode.model_dump())


@router.patch(
    path="/promocode/{id}",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    response_model=PromocodeIn_Pydantic,
    status_code=200
)
async def update_promocode(id: int, promocode: UpdatePromocode):
    if not await Promocode.get_or_none(id=id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await Promocode.filter(id=id).update(**promocode.model_dump(exclude_unset=True))

    return await PromocodeIn_Pydantic.from_queryset(Promocode.filter(id=id).first())


@router.delete(
    path="/promocode/{id}",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    status_code=200
)
async def delete_promocode(id: int):
    if not await Promocode.get_or_none(id=id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await Promocode.filter(id=id).delete()


@router.get(
    path="/promocode/{name}/use",
    response_model=PromocodeIn_Pydantic,
    status_code=200
)
async def apply_promocode(name: str):
    """name - введенный пользователем промокод"""
    promocode: Promocode = await Promocode.get_or_none(name=name)

    if not promocode:
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    if not await promocode.active():
        raise HTTPException(status_code=404, detail="PROMO_INACTIVE")

    await promocode.use()

    return await PromocodeIn_Pydantic.from_tortoise_orm(promocode)
