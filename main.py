from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from tortoise.contrib.fastapi import register_tortoise

from data.config import Config

from utils.storage import create_storage


TORTOISE_MODELS = [
    "database.models.user",
    "database.models.token",
    "database.models.category",
    "database.models.product",
    "database.models.shop_cart",
    "database.models.subcategory",
    "database.models.promocode",
    "database.models.order",
    "database.models.review",
    "aerich.models"
]

TORTOISE_CONFIG = {
    "connections": {
        "default": Config.DB_CONN_STRING
    },
    "apps": {
        "axegaoshop": {
            "models": TORTOISE_MODELS,
            "default_connection": "default"
        }
    }
}

#
# @asynccontextmanager
# async def on_startup(app_: FastAPI):
#     # создание хранилища
#
#
#     yield

app = FastAPI(description="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTA1MjEzNDYsInN1YiI6IjIifQ.AGkvz34_xyFdNMhKf3tK5XwFWNE0pjCr2gAM_abE8W4")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Tortoise.init_models(TORTOISE_MODELS, "axegaoshop")

register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True
)

from routes import users, products, uploads, product_options, product_parameters, product_photos, \
    shop_cart, categories, subcategories, promocodes

app.include_router(router=users.router, prefix="")

app.include_router(router=categories.router, prefix="")

app.include_router(router=subcategories.router, prefix="")

app.include_router(router=products.router, prefix="")
app.include_router(router=product_options.router, prefix="")
app.include_router(router=product_parameters.router, prefix="")
app.include_router(router=product_photos.router, prefix="")

app.include_router(router=promocodes.router)

app.include_router(router=shop_cart.router, prefix="")

app.include_router(router=uploads.router, prefix="")


create_storage()

# @app.get("/", response_model=HealthResponse)
# async def health():
#     return HealthResponse(status="Ok")
