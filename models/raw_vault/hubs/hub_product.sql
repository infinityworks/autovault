{{ config(
  materialized='incremental',
  schema = "HUBS",
  alias = "PRODUCT"
  ) }}

{%- set source_model = ["stg_customer_purchase_history_v0_1_0",
                        "stg_customer_purchase_history_v0_2_0",
                        "stg_products_v0_1_0",
                        "stg_transactions_v0_1_0",
                        "stg_transactions_v0_2_0"] -%}
{%- set src_pk = "PRODUCT_HK" -%}
{%- set src_nk = ["PRODUCT_ID"] -%}
{%- set src_ldts = "LOAD_DATETIME" -%}
{%- set src_source = "RECORD_SOURCE" -%}

{{ dbtvault.hub(src_pk=src_pk,
                src_nk=src_nk,
                src_ldts=src_ldts,
                src_source=src_source,
                source_model=source_model) }}
