from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "reviews" ADD "product_id" INT;
        ALTER TABLE "reviews" ADD CONSTRAINT "fk_reviews_products_9251a0c3" FOREIGN KEY ("product_id") REFERENCES "products" ("id") ON DELETE CASCADE;
        ALTER TABLE "reviews" ADD CONSTRAINT "fk_reviews_orders_72affe1e" FOREIGN KEY ("order_id") REFERENCES "orders" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "reviews" DROP CONSTRAINT "fk_reviews_orders_72affe1e";
        ALTER TABLE "reviews" DROP CONSTRAINT "fk_reviews_products_9251a0c3";
        ALTER TABLE "reviews" DROP COLUMN "product_id";
        CREATE UNIQUE INDEX "uid_reviews_order_i_6eb505" ON "reviews" ("order_id");"""
