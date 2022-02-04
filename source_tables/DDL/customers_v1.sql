CREATE TABLE "AUTOVAULT"."PUBLIC"."CUSTOMERS_V1" (
    "CUSTOMER_ID" {'type': 'STRING', 'tests': {'uniqueness': True, 'nullable': True}},
    "AVG_MONTHLY_VISITS" STRING,
    "RECORD_SOURCE" STRING,
    "LOAD_DATETIME" TIMESTAMP_TZ
    );
