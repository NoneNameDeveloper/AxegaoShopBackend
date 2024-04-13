from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "ticket_messages" ADD "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        CREATE TABLE IF NOT EXISTS "ticket_attachments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "file" TEXT NOT NULL,
    "ticket_id" INT NOT NULL REFERENCES "ticket_messages" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "ticket_attachments" IS 'прикрепленные файлы к сообщениям в ТП';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "ticket_messages" DROP COLUMN "created_at";
        DROP TABLE IF EXISTS "ticket_attachments";"""
