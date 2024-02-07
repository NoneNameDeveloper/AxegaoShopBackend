from fastapi import APIRouter, HTTPException, Depends

from axegaoshop.db.models.order import Order
from axegaoshop.db.models.review import Review, ReviewPhoto
from axegaoshop.db.models.user import User
from axegaoshop.web.api.orders.schema import OrderIn_Pydantic

from axegaoshop.web.api.reviews.schema import ReviewIn_Pydantic, ReviewCreate, ReviewInAdmin_Pydantic, \
     ReviewOutput

from axegaoshop.services.security.jwt_auth_bearer import JWTBearer
from axegaoshop.services.security.users import current_user_is_admin, get_current_user
from axegaoshop.web.api.users.schema import UserProductsComment

router = APIRouter()


@router.post(
    "/reviews/available",
    dependencies=[Depends(JWTBearer())],
    response_model=list[UserProductsComment]
)
async def get_available_reviews_produts(user: User = Depends(get_current_user)):
    """получение доступных для написания отзывов товаров"""
    return [UserProductsComment(id=p[0], title=p[1], order_id=p[2]) for p in await user.get_available_products_to_comment()]


@router.post(
    "/reviews",
    dependencies=[Depends(JWTBearer())],
    status_code=201
)
async def create_review(review_data: ReviewCreate, user: User = Depends(get_current_user)):
    """отправка отзыва (на модерацию)"""
    order = await Order.get_or_none(id=review_data.order_id)

    if not order:
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    if not (await order.user.get_or_none()).id == user.id:
        raise HTTPException(status_code=404, detail="FORIBDDEN")

    if not await order.review_available():
        raise HTTPException(status_code=401, detail="NOT_AVAILABLE")

    review = await Review.create(
        rate=review_data.rate,
        text=review_data.text,
        user=user,
        order_id=review_data.order_id,
    )

    if review_data.images:
        for photo in review_data.images:
            await ReviewPhoto.create(
                review=review,
                photo=photo
            )


@router.get(
    "/reviews/unaccepted",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    response_model=list[ReviewInAdmin_Pydantic]
)
async def get_unaccepted_reviews():
    return await ReviewInAdmin_Pydantic.from_queryset(Review.filter(accepted=False))


@router.get(
    "/reviews",
    response_model=list[ReviewOutput]

)
async def get_reviews():
    return [
        ReviewOutput(images=[photo.photo for photo in r.review_photos], rate=r.rate, text=r.text) for r in await Review.filter(accepted=True).prefetch_related("review_photos").all()
    ]


@router.patch(
    "/reviews/{review_id}",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    response_model=ReviewIn_Pydantic
)
async def update_review():
    """:TODO: НЕ СДЕЛАНО - обновление отзыва из админки и сохранение"""
    ...