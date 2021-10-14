{%- set yaml_metadata -%}
source_model:
  AUTOVAULT_PUBLIC: "TRANSACTIONS_V1"
derived_columns:
  EFFECTIVE_FROM: "LOAD_DATETIME"
  START_DATE: "LOAD_DATETIME"
  END_DATE: "TO_DATE('9999-12-31')"
hashed_columns:
  TRANSACTIONS_HK: "CUSTOMER_ID"
  TRANSACTIONS_HASHDIFF
    is_hashdiff: true
    columns:
      - "CUSTOMER_ID"
      - "DATE_OF_SESSION"
      - "PRODUCTS_VIEWED"
      - "PRICE"
      - "PRODUCT_ID"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.stage(include_source_columns=true,
                  source_model=metadata_dict['source_model'],
                  derived_columns=metadata_dict['derived_columns'],
                  hashed_columns=metadata_dict['hashed_columns'],
                  ranked_columns=none) }}
