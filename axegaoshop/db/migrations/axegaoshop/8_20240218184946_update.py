from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "replenishes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "number" VARCHAR(50) NOT NULL UNIQUE,
    "result_price" DECIMAL(10,2),
    "payment_type" VARCHAR(100) NOT NULL,
    "status" VARCHAR(100) NOT NULL  DEFAULT 'waiting_payment',
    "created_datetime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "payed_datetime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "replenishes" IS 'таблица с пополнениями баланса';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "replenishes";"""
