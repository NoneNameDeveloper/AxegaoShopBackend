from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "parameters" ADD "give_type" VARCHAR(30) NOT NULL  DEFAULT 'string';
        ALTER TABLE "products" DROP COLUMN "give_type";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "products" ADD "give_type" VARCHAR(30) NOT NULL  DEFAULT 'string';
        ALTER TABLE "parameters" DROP COLUMN "give_type";"""
