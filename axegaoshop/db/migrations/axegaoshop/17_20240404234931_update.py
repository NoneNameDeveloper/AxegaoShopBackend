from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "product_data" ADD "order_id" INT;
        ALTER TABLE "product_data" ADD CONSTRAINT "fk_product__orders_14b9de5f" FOREIGN KEY ("order_id") REFERENCES "orders" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "product_data" DROP CONSTRAINT "fk_product__orders_14b9de5f";
        ALTER TABLE "product_data" DROP COLUMN "order_id";"""
