{{ config(
  materialized='incremental',
  schema = "HUBS",
  alias = "TRANSACTION"
  ) }}

{%- set source_model = ["stg_transactions_v1"] -%}
{%- set src_pk = "TRANSACTION_HK" -%}
{%- set src_nk = ["DATE_OF_SESSION",
                  "PRODUCT_ID"] -%}
{%- set src_ldts = "LOAD_DATETIME" -%}
{%- set src_source = "RECORD_SOURCE" -%}

{{ dbtvault.hub(src_pk=src_pk,
                src_nk=src_nk,
                src_ldts=src_ldts,
                src_source=src_source,
                source_model=source_model) }}
