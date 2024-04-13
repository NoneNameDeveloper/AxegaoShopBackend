from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "payment_settings_ozone" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT,
    "token" TEXT NOT NULL,
    "pin_code" TEXT NOT NULL,
    "created_datetime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "phone" TEXT NOT NULL,
    "fio" TEXT NOT NULL
);
COMMENT ON TABLE "payment_settings_ozone" IS 'таблица с данными о платежке Sbp OzoneBank';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "payment_settings_ozone";"""
