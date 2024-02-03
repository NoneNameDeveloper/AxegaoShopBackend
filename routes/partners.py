from fastapi import APIRouter, Depends, HTTPException

from database.models.partner import Partner
from security.auth_bearer import JWTBearer
from utils.users_misc import current_user_is_admin

from schemas.partners import CreatePartner, PartnerIn_Pydantic


router = APIRouter(tags=["Partners"])


@router.post(
    "/partners",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    status_code=201
)
async def create_partner(partner: CreatePartner):
    await Partner.create(**partner.model_dump())


@router.delete(
    "/partner/{id}",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    status_code=200
)
async def delete_partner(id: int):
    partner = await Partner.get_or_none(id=id)

    if not partner:
        raise HTTPException(status_code=404, detail="PARTNER_NOT_FOUND")

    await partner.delete()


@router.get(
    "partners",
    status_code=200,
    response_model=list[PartnerIn_Pydantic]
)
async def get_partners():
    return await PartnerIn_Pydantic.from_queryset(Partner.all())
