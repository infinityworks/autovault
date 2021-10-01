{%- set yaml_metadata -%}
source_model: 
  AV: "TOTAL_CUST_VISITS"
derived_columns:
  CUSTOMER_ID: "CUST_ID"
  EFFECTIVE_FROM: "LOAD_DATE"
  START_DATE: "LOAD_DATE"
  END_DATE: "TO_DATE('2050-12-31')"
hashed_columns:
  CUSTOMER_HK: "CUSTOMER_ID"
  TOTAL_CUST_VISITS_HASHDIFF:
    is_hashdiff: true
    columns:
      - "TOTAL_VISITS"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.stage(include_source_columns=true,
                  source_model=metadata_dict['source_model'],
                  derived_columns=metadata_dict['derived_columns'],
                  hashed_columns=metadata_dict['hashed_columns'],
                  ranked_columns=none) }}
