{{ config(
  materialized='incremental',
  schema = "LINK",
  alias = "CUST_PRDCT_CUST_HISTORY"
  ) }}

{%- set yaml_metadata -%}
source_model:
  - "stg_customer_purchase_history_v0_1_0"
src_pk:
  - "CUST_PRDCT_CUST_HISTORY_HK"
src_fk:
  - "CUSTOMER_HK"
  - "PRODUCT_HK"
src_ldts: "LOAD_DATETIME"
src_source: "RECORD_SOURCE"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.link(src_pk=src_pk, src_fk=src_fk, src_ldts=src_ldts,
                 src_source=src_source, source_model=source_model) }}
