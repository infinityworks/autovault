CREATE TABLE "AUTOVAULT"."PUBLIC"."TRANSACTIONS_V1" (
    "CUSTOMER_ID" {'alias': 'CUSTOMER_ID', 'type': 'STRING', 'tests': {'uniqueness': True, 'nullable': True}},
    "DATE_OF_SESSION" {'type': 'TIMESTAMP_TZ(9)'},
    "PRODUCT_ID" {'type': 'STRING'},
    "PRICE" NUMBER,
    "RECORD_SOURCE" STRING,
    "LOAD_DATETIME" TIMESTAMP_TZ
    );
