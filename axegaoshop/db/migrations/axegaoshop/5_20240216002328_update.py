from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "password_resets" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "is_active" BOOL NOT NULL
);
COMMENT ON TABLE "password_resets" IS 'таблица сбросов пароля (можно использовать ссылку единожды)';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "password_resets";"""
