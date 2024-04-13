from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255),
    "email" VARCHAR(255),
    "balance" DECIMAL(10,2) NOT NULL  DEFAULT 0,
    "photo" VARCHAR(255) NOT NULL,
    "reg_datetime" TIMESTAMPTZ NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_anonymous" BOOL NOT NULL  DEFAULT False,
    "is_admin" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "tokens" (
    "user_id" INT NOT NULL,
    "created_datetime" TIMESTAMPTZ NOT NULL,
    "access_token" VARCHAR(500) NOT NULL  PRIMARY KEY,
    "refresh_token" VARCHAR(500) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True
);
CREATE TABLE IF NOT EXISTS "categories" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_datetime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(500) NOT NULL,
    "photo" VARCHAR(200),
    "order_id" INT NOT NULL
);
COMMENT ON TABLE "categories" IS 'таблица с категориями';
CREATE TABLE IF NOT EXISTS "subcategories" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_datetime" TIMESTAMPTZ NOT NULL,
    "title" VARCHAR(500) NOT NULL,
    "order_id" INT NOT NULL,
    "category_id" INT NOT NULL REFERENCES "categories" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "subcategories" IS 'таблица с подкатегориями';
CREATE TABLE IF NOT EXISTS "products" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_datetime" TIMESTAMPTZ NOT NULL,
    "title" VARCHAR(500) NOT NULL,
    "description" TEXT NOT NULL,
    "card_price" DECIMAL(10,2) NOT NULL,
    "card_has_sale" BOOL NOT NULL  DEFAULT False,
    "card_sale_price" DECIMAL(10,2) NOT NULL,
    "give_type" VARCHAR(30) NOT NULL  DEFAULT 'string',
    "order_id" BIGINT NOT NULL,
    "subcategory_id" INT NOT NULL REFERENCES "subcategories" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "products" IS 'таблица с товарами (винда 11, винда 10...)';
CREATE TABLE IF NOT EXISTS "options" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "value" TEXT NOT NULL,
    "is_pk" BOOL NOT NULL  DEFAULT False,
    "product_id" INT NOT NULL REFERENCES "products" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "options" IS 'таблица с характеристиками (код, метод установки...)';
CREATE TABLE IF NOT EXISTS "parameters" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "price" DECIMAL(10,2) NOT NULL,
    "has_sale" BOOL NOT NULL  DEFAULT False,
    "sale_price" DECIMAL(10,2) NOT NULL,
    "order_id" INT NOT NULL,
    "product_id" INT NOT NULL REFERENCES "products" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "parameters" IS 'таблица с параметрами - версиями товара (винда домашняя, винда профессиональная...)';
CREATE TABLE IF NOT EXISTS "product_data" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "value" TEXT NOT NULL,
    "parameter_id" INT NOT NULL REFERENCES "parameters" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "product_data" IS 'таблица с самими товарами (ключами..)';
CREATE TABLE IF NOT EXISTS "product_photos" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "photo" VARCHAR(200) NOT NULL,
    "main" BOOL NOT NULL  DEFAULT False,
    "product_id" INT NOT NULL REFERENCES "products" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "product_photos" IS 'фотографии к товарам';
CREATE TABLE IF NOT EXISTS "shop_cart" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "quantity" INT NOT NULL  DEFAULT 1,
    "parameter_id" INT NOT NULL REFERENCES "parameters" ("id") ON DELETE CASCADE,
    "product_id" INT NOT NULL REFERENCES "products" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "promocodes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "activations_count" INT NOT NULL  DEFAULT 1,
    "sale_percent" DOUBLE PRECISION NOT NULL,
    "created_datetime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "promocodes" IS 'таблица с промокодами';
CREATE TABLE IF NOT EXISTS "orders" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "number" VARCHAR(50) NOT NULL UNIQUE,
    "straight" BOOL NOT NULL  DEFAULT True,
    "result_price" DECIMAL(10,2),
    "status" VARCHAR(100) NOT NULL  DEFAULT 'waiting_payment',
    "email" TEXT NOT NULL,
    "payment_type" VARCHAR(100) NOT NULL,
    "promocode_id" INT REFERENCES "promocodes" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "orders" IS 'таблица с заказами';
CREATE TABLE IF NOT EXISTS "order_parameters" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "count" INT NOT NULL  DEFAULT 1,
    "order_id" INT NOT NULL REFERENCES "orders" ("id") ON DELETE CASCADE,
    "parameter_id" INT NOT NULL REFERENCES "parameters" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "order_parameters" IS 'таблица с находящимися в заказе това то, но возможно то рами (версиями товара) - параметры заказа';
CREATE TABLE IF NOT EXISTS "reviews" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "status" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    "rate" INT NOT NULL,
    "created_datetime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "approved_datetime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "order_id" INT NOT NULL UNIQUE REFERENCES "orders" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "review_photos" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "photo" TEXT NOT NULL,
    "review_id" INT NOT NULL REFERENCES "reviews" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "partners" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_datetime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "photo" VARCHAR(100) NOT NULL
);
COMMENT ON TABLE "partners" IS 'таблица с партнерами (фоторгафии полноразмерные, сжимаются для';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
