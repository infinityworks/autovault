{{ config(
  materialized='incremental',
  schema = "HUBS",
  alias = "CUSTOMER"
  ) }}

{%- set source_model = ["stg_customer_purchase_history_v0_1_0",
                        "stg_customer_purchase_history_v0_2_0",
                        "stg_customers_v0_1_0",
                        "stg_customers_v0_1_1",
                        "stg_transactions_v0_1_0",
                        "stg_transactions_v0_2_0"] -%}
{%- set src_pk = "CUSTOMER_HK" -%}
{%- set src_nk = ["CUSTOMER_ID"] -%}
{%- set src_ldts = "LOAD_DATETIME" -%}
{%- set src_source = "RECORD_SOURCE" -%}

{{ dbtvault.hub(src_pk=src_pk,
                src_nk=src_nk,
                src_ldts=src_ldts,
                src_source=src_source,
                source_model=source_model) }}
