from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "product_data" ADD "is_active" BOOL NOT NULL  DEFAULT True;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "product_data" DROP COLUMN "is_active";"""
