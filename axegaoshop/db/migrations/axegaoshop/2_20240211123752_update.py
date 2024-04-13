from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "orders" ADD "created_datetime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "orders" DROP COLUMN "created_datetime";"""
