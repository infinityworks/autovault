{{ config(
  materialized='incremental',
  schema = "$model_type",
  alias = "$effsat_name"
  ) }}

{%- set source_model = $source_model  -%}
{%- set src_pk = "$src_pk"  -%}
{%- set src_dfk = "$src_dfk"        -%}
{%- set src_sfk = [$src_fk]          -%}
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
