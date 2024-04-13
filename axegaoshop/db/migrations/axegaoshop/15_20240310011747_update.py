from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "ticket_attachments" RENAME COLUMN "ticket_id" TO "ticket_message_id";
        ALTER TABLE "ticket_attachments" ADD CONSTRAINT "fk_ticket_a_ticket_m_14b1a5ea" FOREIGN KEY ("ticket_message_id") REFERENCES "ticket_messages" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "ticket_attachments" DROP CONSTRAINT "fk_ticket_a_ticket_m_14b1a5ea";
        ALTER TABLE "ticket_attachments" RENAME COLUMN "ticket_message_id" TO "ticket_id";
        ALTER TABLE "ticket_attachments" ADD CONSTRAINT "fk_ticket_a_ticket_m_a3c91972" FOREIGN KEY ("ticket_id") REFERENCES "ticket_messages" ("id") ON DELETE CASCADE;"""
