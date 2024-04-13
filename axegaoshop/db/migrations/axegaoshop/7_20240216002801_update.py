from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "password_resets" ADD "hashed_password" TEXT NOT NULL;
        ALTER TABLE "password_resets" ADD "email" TEXT NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "password_resets" DROP COLUMN "hashed_password";
        ALTER TABLE "password_resets" DROP COLUMN "email";"""
