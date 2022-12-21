{{ config(
  materialized='incremental',
  schema = "$model_type",
  alias = "$alias"
  ) }}

{%- set yaml_metadata -%}
source_model:
$source_model
src_pk:
$src_pk
src_fk:
$src_fk
src_ldts: "$src_ldts"
src_source: "$src_source"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.link(src_pk=src_pk, src_fk=src_fk, src_ldts=src_ldts,
                 src_source=src_source, source_model=source_model) }}
