{{
  config(materialized='view',
  schema = "STAGING"
  ) }}

{%- set yaml_metadata -%}
source_model:
  AUTOVAULT_PUBLIC: "TRANSACTIONS_V0_1_0"
derived_columns:
  EFFECTIVE_FROM: "LOAD_DATETIME"
  START_DATE: "LOAD_DATETIME"
  END_DATE: "TO_DATE('9999-12-31')"

hashed_columns:
  CUSTOMER_HK:
    - "CUSTOMER_ID"
  PRODUCT_HK:
    - "PRODUCT_ID"
  TRANSACTION_HK:
    - "DATE_OF_SESSION"
    - "CUSTOMER_ID"
  CUST_PRDCT_TRNSCTN_CUST_CHECKOUT_HK:
    - "CUSTOMER_ID"
    - "DATE_OF_SESSION"
    - "PRODUCT_ID"
  PRODUCTS_HASHDIFF:
    is_hashdiff: true
    columns:
      - "PRICE"

{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.stage(include_source_columns=true,
                  source_model=metadata_dict['source_model'],
                  derived_columns=metadata_dict['derived_columns'],
                  hashed_columns=metadata_dict['hashed_columns'],
                  ranked_columns=none) }}
