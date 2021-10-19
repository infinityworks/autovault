
{{ config(
  materialized='incremental',
  schema = "HUBS"
  ) }}

{%- set source_model = [$source_model] -%}
{%- set src_pk = "$src_pk" -%}
{%- set src_nk = "$src_nk" -%}
{%- set src_ldts = "$src_ldts" -%}
{%- set src_source = "$src_source" -%}

{{ dbtvault.hub(src_pk=src_pk,
                src_nk=src_nk,
                src_ldts=src_ldts,
                src_source=src_source,
                source_model=source_model) }}
