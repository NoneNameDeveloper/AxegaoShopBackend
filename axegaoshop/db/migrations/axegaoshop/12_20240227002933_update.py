from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tickets" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "status" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "closed_at" TIMESTAMPTZ,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "tickets" IS 'таблица с данными по тикетам';
        CREATE TABLE IF NOT EXISTS "ticket_messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "role" VARCHAR(20) NOT NULL,
    "text" TEXT NOT NULL,
    "ticket_id" INT NOT NULL REFERENCES "tickets" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "ticket_messages" IS 'таблица с диалогами и сообщениями админа/юзера';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "tickets";
        DROP TABLE IF EXISTS "ticket_messages";"""
