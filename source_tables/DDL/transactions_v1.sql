CREATE TABLE "AUTOVAULT"."PUBLIC"."TRANSACTIONS_V1" (
    "CUSTOMER_ID" {'type': 'STRING', 'tests': {'uniqueness': True, 'nullable': True}},
    "DATE_OF_SESSION" {'type': 'TIMESTAMP_TZ(9)', 'tests': {'uniqueness': True, 'nullable': True}},
    "PRODUCT_ID" {'type': 'STRING', 'tests': {'uniqueness': True, 'nullable': True}},
    "PRICE" {'type': 'NUMBER', 'tests': {'uniqueness': True, 'nullable': True}},
    "RECORD_SOURCE" STRING,
    "LOAD_DATETIME" TIMESTAMP_TZ
    );
