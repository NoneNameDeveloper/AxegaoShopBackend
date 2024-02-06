import typing

from fastapi import APIRouter, Depends, HTTPException
from tortoise.functions import Avg

from axegaoshop.db.models.product import Product, Parameter, Option, ProductPhoto, ProductData, change_product_order
from axegaoshop.db.models.subcategory import Subcategory

from axegaoshop.web.api.products.schema import ProductCreate, ProductIn_Pydantic, ProductOrderChange

from axegaoshop.services.security.jwt_auth_bearer import JWTBearer
from axegaoshop.services.security.users import current_user_is_admin

router = APIRouter()


@router.get(
    "/products",
    status_code=200,
    response_model=list[ProductIn_Pydantic]
)
async def get_products(
        price_sort: bool = False,
        rating_sort: bool = False,
        sale_sort: bool = False,
        query: typing.Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
):
    """
    Поиск карточек товара в базе данных для админа и пользователей:

    *query* - вхождение (startswith) в title (название) товара (не чувствителен к регистру)
    """

    if not query:
        sorted_products = (Product.all().prefetch_related()
                               .limit(limit)
                               .offset(offset)

                               .order_by("card_price" if price_sort else "-card_price")
                               .annotate(param_reviews_count=Avg('parameters__reviews__rate'))
                               .order_by("param_reviews_count" if rating_sort else "-param_reviews_count")
                           )
        sorted_products = sorted_products.filter(card_has_sale=True) if sale_sort else \
            sorted_products

        return await ProductIn_Pydantic.from_queryset(sorted_products)
    else:
        return await ProductIn_Pydantic.from_queryset(Product.filter(title__istartswith=query).
                                                      limit(limit).
                                                      offset(offset))


@router.get(
    "/subcategory/{subcategory_id}/products",
    response_model=list[ProductIn_Pydantic]
)
async def subcategory_products_get(
        subcategory_id: int,
        price_sort: bool = False,
        rating_sort: bool = False,
        sale_sort: bool = False,
        limit: int = 20,
        offset: int = 0,
):
    """
    Получение товаров из подкатегории
    """
    if not await Subcategory.get_or_none(id=subcategory_id):
        raise HTTPException(status_code=404, detail="SUBCATEGORY_NOT_FOUND")

    sorted_products = (Product.filter(subcategory_id=subcategory_id)
                       .limit(limit)
                       .offset(offset)
                       .order_by("card_price" if price_sort else "-card_price")
                       .order_by("parameters__reviews__rate" if rating_sort else "-parameters__reviews__rate")
                       )
    sorted_products = sorted_products.filter(card_has_sale=True) if sale_sort else \
        sorted_products

    return await ProductIn_Pydantic.from_queryset(sorted_products)


@router.post(
    "/product/",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    status_code=201
)
async def create_product(
        product_data: ProductCreate
):
    photos_ = product_data.photos
    options_ = product_data.options
    parameters_ = product_data.parameters

    subcategory = await Subcategory.filter(id=product_data.subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="CATEGORY_NOT_FOUND")

    product = Product(
        title=product_data.title,
        description=product_data.description,
        card_price=product_data.card_price,
        card_has_sale=parameters_[0].has_sale,
        card_sale_price=parameters_[0].sale_price,
        give_type=product_data.give_type,
        subcategory=subcategory
    )

    await product.save()

    parameters = [Parameter(
        title=p.title,
        price=p.price,
        has_sale=p.has_sale,
        sale_price=p.sale_price,
        product=product
    ) for p in parameters_]

    for param in parameters:
        await param.save()
        for p in parameters_:
            for d in p.data:
                p_d = ProductData(
                    parameter=param,
                    value=d.value
                )
                await p_d.save()

    if options_:
        options = [Option(
            title=o.title,
            value=o.value,
            is_pk=o.is_pk,
            product=product
        ) for o in options_]

        # saving options
        if all([await opt.is_available() for opt in options]):
            for opt in options:
                await opt.save()

    product_photo = [ProductPhoto(
        photo=pp.photo,
        product=product
    ) for pp in photos_]

    for pht in product_photo:
        await pht.save()

    return {"id": product.id}


@router.get(
    "/product/{id}",
    dependencies=[Depends(JWTBearer())],
    response_model=ProductIn_Pydantic
)
async def get_product(id: int):
    product_ = await Product.get_or_none(id=id)

    if not product_:
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    return await ProductIn_Pydantic.from_queryset_single(Product.get(id=id))


@router.delete(
    "/product/{id}",
    description="Delete product and all related data",
    status_code=200
)
async def delete_product(id: int):
    product_ = await Product.get_or_none(id=id)

    if not product_:
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    await product_.delete()


@router.post(
    "/product/order",
    dependencies=[Depends(JWTBearer()), Depends(current_user_is_admin)],
    status_code=200
)
async def change_product_order_router(product_order: ProductOrderChange):
    res = await change_product_order(product_order.product_1, product_order.product_2)

    if not res:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
