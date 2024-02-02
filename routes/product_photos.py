from fastapi import APIRouter, HTTPException, Depends

from database.models.product import ProductPhoto, Product
from schemas.products import PhotoIn_Pydantic, PhotoCreate, PhotoUpdate
from security.auth_bearer import JWTBearer
from utils.users_misc import current_user_is_admin

router = APIRouter(tags=["Product Photos"])


@router.get(
    path="/product/{id}/photos",
    response_model=list[PhotoIn_Pydantic]
)
async def get_product_photo(id: int):
    if not await Product.get_or_none(id=id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    return await PhotoIn_Pydantic.from_queryset(ProductPhoto.filter(product_id=id))


@router.post(
    path="/product/{id}/photos",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    response_model=PhotoIn_Pydantic
)
async def create_product_photo(id: int, photo: PhotoCreate):
    if not await Product.get_or_none(id=id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    photo_ = ProductPhoto(
        photo=photo.title,
        product_id=id
    )

    await photo_.save()

    return photo_


@router.patch(
    path="/photo/{id}",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    response_model=PhotoIn_Pydantic
)
async def update_product_photo(id: int, parameter: PhotoUpdate):
    if not await ProductPhoto.get_or_none(id=id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await ProductPhoto.filter(id=id).update(**parameter.model_dump(exclude_unset=True))

    return await ProductPhoto.filter(id=id).first()


@router.delete(
    path="/photo/{id}",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    status_code=200
)
async def delete_product_photo(id: int):
    if not await ProductPhoto.get_or_none(id=id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await ProductPhoto.filter(id=id).delete()
