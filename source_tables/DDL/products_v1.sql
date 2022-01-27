CREATE TABLE "AUTOVAULT"."PUBLIC"."PRODUCTS_V1" (
    "PRODUCT_ID" {'alias': 'PRODUCT_ID', 'type': 'STRING', 'tests': {'uniqueness': True, 'nullable': True}},
    "MAKE" STRING,
    "MODEL" STRING,
    "RECORD_SOURCE" STRING,
    "LOAD_DATETIME" TIMESTAMP_TZ
    );
