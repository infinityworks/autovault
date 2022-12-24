{{
  config(materialized='view',
  schema = "STAGING"
  ) }}

{%- set yaml_metadata -%}
source_model:
  AUTOVAULT_PUBLIC: "CUSTOMERS_V0_1_1"
derived_columns:
  EFFECTIVE_FROM: "LOAD_DATETIME"
  START_DATE: "LOAD_DATETIME"
  END_DATE: "TO_TIMESTAMP_TZ('9999-01-01 00:00:00')"

hashed_columns:
  CUSTOMER_HK:
    - "CUSTOMER_ID"

  CUSTOMER_DETAILS_HASHDIFF:
    is_hashdiff: true
    columns:
      - "AGE"

{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.stage(include_source_columns=true,
                  source_model=metadata_dict['source_model'],
                  derived_columns=metadata_dict['derived_columns'],
                  hashed_columns=metadata_dict['hashed_columns'],
                  ranked_columns=none) }}
