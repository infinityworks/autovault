{{ config(
  materialized='incremental',
  schema = "EFFSATS",
  alias = "CUST_PRDCT_STORE_CHECKOUT_v0_1_0"
  ) }}

{%- set source_model = "stg_transactions_v0_1_0"  -%}
{%- set src_pk = "CUST_PRDCT_STORE_CHECKOUT_HK"  -%}
{%- set src_dfk = "CUSTOMER_HK"        -%}
{%- set src_sfk = ["PRODUCT_HK"]          -%}
{%- set src_start_date = "START_DATE" -%}
{%- set src_end_date = "END_DATE"     -%}

{%- set src_eff = "EFFECTIVE_FROM"    -%}
{%- set src_ldts = "LOAD_DATETIME"    -%}
{%- set src_source = "RECORD_SOURCE"  -%}

{{ dbtvault.eff_sat(src_pk=src_pk, src_dfk=src_dfk, src_sfk=src_sfk,
                    src_start_date=src_start_date,
                    src_end_date=src_end_date,
                    src_eff=src_eff, src_ldts=src_ldts,
                    src_source=src_source,
                    source_model=source_model) }}
