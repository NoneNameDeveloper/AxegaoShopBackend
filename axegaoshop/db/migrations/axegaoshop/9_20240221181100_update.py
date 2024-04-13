from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "telegram_recievers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "telegram_id" BIGINT NOT NULL
);
COMMENT ON TABLE "telegram_recievers" IS 'таблица с получателями уведов в телеграммк';
        CREATE TABLE IF NOT EXISTS "telegram_settings" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" TEXT NOT NULL
);
COMMENT ON TABLE "telegram_settings" IS 'таблица с данными об уведомлениях в телеграмм';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "telegram_recievers";
        DROP TABLE IF EXISTS "telegram_settings";"""
