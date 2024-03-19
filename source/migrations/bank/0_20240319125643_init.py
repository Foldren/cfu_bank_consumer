from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "support_banks" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(8) NOT NULL,
    "logo_url" TEXT
);
COMMENT ON COLUMN "support_banks"."name" IS 'Название банка';
CREATE TABLE IF NOT EXISTS "user_banks" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" VARCHAR(100) NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "token" BYTEA NOT NULL,
    "support_bank_id" BIGINT NOT NULL REFERENCES "support_banks" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_user_banks_user_id_53b51e" ON "user_banks" ("user_id");
CREATE TABLE IF NOT EXISTS "payment_accounts" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "legal_entity_id" VARCHAR(100) NOT NULL,
    "start_date" DATE,
    "number" VARCHAR(50) NOT NULL UNIQUE,
    "balance" VARCHAR(30)   DEFAULT '0',
    "status" SMALLINT NOT NULL  DEFAULT 1,
    "user_bank_id" BIGINT NOT NULL REFERENCES "user_banks" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_payment_acc_legal_e_1019c2" ON "payment_accounts" ("legal_entity_id");
COMMENT ON COLUMN "payment_accounts"."status" IS 'Статус расчётного счета';
CREATE TABLE IF NOT EXISTS "data_collects" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "trxn_date" DATE NOT NULL,
    "counterparty_name" VARCHAR(100) NOT NULL,
    "counterparty_inn" VARCHAR(30)   DEFAULT '',
    "type" VARCHAR(6) NOT NULL,
    "amount" DECIMAL(19,2) NOT NULL,
    "payment_account_id" BIGINT NOT NULL REFERENCES "payment_accounts" ("id") ON DELETE CASCADE,
    "support_bank_id" BIGINT NOT NULL REFERENCES "support_banks" ("id") ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS "idx_data_collec_trxn_da_755215" ON "data_collects" ("trxn_date");
COMMENT ON COLUMN "data_collects"."type" IS 'Тип операции';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
