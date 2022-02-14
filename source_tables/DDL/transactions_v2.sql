CREATE TABLE "AUTOVAULT"."PUBLIC"."TRANSACTIONS_V2" (
    "CUSTOMER_ID" {'type': 'STRING', 'tests': {'uniqueness': True, 'nullable': True}},
    "PRODUCT_ID" {'type': 'STRING', 'tests': {'uniqueness': True, 'nullable': True}},
    "PRICE" {'type': 'NUMBER', 'tests': {'uniqueness': True, 'nullable': True}},
    "RECORD_SOURCE" STRING,
    "LOAD_DATETIME" TIMESTAMP_TZ
    );
