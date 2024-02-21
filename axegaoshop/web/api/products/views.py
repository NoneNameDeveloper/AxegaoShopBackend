import typing

from fastapi import APIRouter, Depends, HTTPException
from tortoise.functions import Avg, Coalesce

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
        price_sort: typing.Optional[bool] = None,
        rating_sort: typing.Optional[bool] = None,
        sale_sort: typing.Optional[bool] = None,
        query: typing.Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
):
    """
    Поиск карточек товара в базе данных для админа и пользователей:

    *query* - вхождение (startswith) в title (название) товара (не чувствителен к регистру)

    если *price_sort*, *rating_sort*, *sale_sort* не переданы, используется стандартный order, заданный админом

    *price_sort*, *rating_sort*, *sale_sort* могут принимать значения true/false или просто их не указывать
    """

    if not query:
        sorted_products = (Product.filter().all().prefetch_related()
                           .limit(limit)
                           .offset(offset)
                           )
        if price_sort or rating_sort:
            sorted_products = (sorted_products
                               .order_by("card_price" if price_sort else "-card_price")
                               .annotate(
                                    param_reviews_count=Coalesce(Avg(
                                        'parameters__order_parameters__order__review__rate'),
                                        0
                                    )
                                )
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
        price_sort: typing.Optional[bool] = None,
        rating_sort: typing.Optional[bool] = None,
        sale_sort: typing.Optional[bool] = None,
        limit: int = 20,
        offset: int = 0,
):
    """
    Получение товаров из поджкатегории

    если *price_sort*, *rating_sort*, *sale_sort* не переданы, используется стандартный order, заданный админом

    *price_sort*, *rating_sort*, *sale_sort* могут принимать значения true/false или просто их не указывать
    """
    if not await Subcategory.get_or_none(id=subcategory_id):
        raise HTTPException(status_code=404, detail="SUBCATEGORY_NOT_FOUND")

    sorted_products = (Product.filter(subcategory_id=subcategory_id).all().prefetch_related()
                       .limit(limit)
                       .offset(offset)
                       )
    if price_sort or rating_sort:
        sorted_products = (sorted_products
                           .order_by("card_price" if price_sort else "-card_price")
                           .annotate(
                                param_reviews_count=Coalesce(Avg(
                                    'parameters__order_parameters__order__review__rate'),
                                    0
                                )
        )
                           .order_by("param_reviews_count" if rating_sort else "-param_reviews_count")
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
    """
    *give_type* - тип выдачи.
      - string - обычные строки
      - file - файлы
      - hand - ручная выдача из админки

    Если тип выдачи *string* - грузим так же, как и в примере.

    Если тип выдачи *file* требуется сначала загрузить файлы в /api/upload
    и результат передать в качестве параметров

    Если тип выдачи *hand* можно исключить ['parameters']['data'] из запроса на создание товара
    """
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
                    value=d
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

    # добавление фото товара и назначение первой фотографии main
    product_photo = [ProductPhoto(
        photo=pp,
        product=product,
        main=True if idx == 0 else False
    ) for idx, pp in enumerate(photos_, start=0)]

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
