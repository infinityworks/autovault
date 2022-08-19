{{ config(
  materialized='incremental',
  schema = "LINKS",
  alias = "CUST_PRDCT_TRNSCTN_CUST_CHECKOUT"
  ) }}

{%- set source_model = ["stg_transactions_v0_1_0"]     -%}
{%- set src_pk = "CUST_PRDCT_TRNSCTN_CUST_CHECKOUT_HK"         -%}
{%- set src_fk = ["CUSTOMER_HK",
                  "PRODUCT_HK",
                  "TRANSACTION_HK"]  -%}
{%- set src_ldts = "LOAD_DATETIME" -%}
{%- set src_source = "RECORD_SOURCE" -%}

{{ dbtvault.link(src_pk=src_pk, src_fk=src_fk, src_ldts=src_ldts,
                 src_source=src_source, source_model=source_model) }}
