{{ config(
  materialized='incremental',
  schema = "HUBS",
  alias = "TRANSACTION"
  ) }}

{%- set source_model = ["stg_transactions_v0_1_0"] -%}
{%- set src_pk = "TRANSACTION_HK" -%}
{%- set src_nk = ["CUSTOMER_ID",
                  "DATE_OF_SESSION"] -%}
{%- set src_ldts = "LOAD_DATETIME" -%}
{%- set src_source = "RECORD_SOURCE" -%}

{{ dbtvault.hub(src_pk=src_pk,
                src_nk=src_nk,
                src_ldts=src_ldts,
                src_source=src_source,
                source_model=source_model) }}
