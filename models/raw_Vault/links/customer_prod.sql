{{ config(materialized='incremental',
  schema = "LINKS"

) }}

{%- set source_model = "stg_transactions" -%}
{%- set src_pk = "LINK_CUSTOMER_PROD_HK" -%}
{%- set src_fk = ["CUSTOMER_HK", "PRODUCT_HK"] -%}
{%- set src_ldts = "LOAD_DATE"           -%}
{%- set src_source = "RECORD_SOURCE"         -%}

{{ dbtvault.link(src_pk=src_pk, src_fk=src_fk, src_ldts=src_ldts,
                 src_source=src_source, source_model=source_model) }}
