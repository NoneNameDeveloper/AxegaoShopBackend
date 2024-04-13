from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "password_resets" ALTER COLUMN "is_active" SET DEFAULT True;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "password_resets" ALTER COLUMN "is_active" DROP DEFAULT;"""
