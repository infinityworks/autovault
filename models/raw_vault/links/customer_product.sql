{{ config(
  materialized='incremental',
  schema = "LINKS"
  ) }}

{%- set source_model = ["stg_PRODUCTS_V1", "stg_PRODUCTS_V2"]     -%}
{%- set src_pk = "CUSTOMER_PRODUCT_HK"         -%}
{%- set src_fk = ["CUSTOMER_HK", "PRODUCT_HK"]  -%}
{%- set src_ldts = "LOAD_DATETIME" -%}
{%- set src_source = "RECORD_SOURCE" -%}

{{ dbtvault.link(src_pk=src_pk, src_fk=src_fk, src_ldts=src_ldts,
                 src_source=src_source, source_model=source_model) }}
