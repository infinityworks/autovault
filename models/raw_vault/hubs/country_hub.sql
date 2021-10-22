
{{ config(
  materialized='incremental',
  schema = "HUBS",
  alias = "COUNTRY"
  ) }}

{%- set source_model = ["stg_products_v2"] -%}
{%- set src_pk = "COUNTRY_HK" -%}
{%- set src_nk = "DEPT_ID" -%}
{%- set src_ldts = "LOAD_DATETIME" -%}
{%- set src_source = "RECORD_SOURCE" -%}

{{ dbtvault.hub(src_pk=src_pk,
                src_nk=src_nk,
                src_ldts=src_ldts,
                src_source=src_source,
                source_model=source_model) }}
