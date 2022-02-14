CREATE TABLE "AUTOVAULT"."PUBLIC"."CUSTOMER_VISITS_V1" (
    "CUST_ID" {'alias': 'CUSTOMER_ID', 'type': 'STRING', 'tests': {'uniqueness': True, 'nullable': True}},
    "TOTAL_VISITS" STRING,
    "RECORD_SOURCE" STRING,
    "LOAD_DATETIME" TIMESTAMP_TZ
    );
