{{ config(
  materialized='incremental',
  schema = "$model_type",
  alias = "$alias"
  ) }}

{%- set yaml_metadata -%}
source_model: $source_model
src_pk:
$src_pk
src_fk:
$src_fk
src_payload:
$payload
src_eff: "EFFECTIVE_FROM"
src_ldts: "$src_ldts"
src_source: "$src_source"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.t_link(src_pk=metadata_dict["src_pk"],
                   src_fk=metadata_dict["src_fk"],
                   src_payload=metadata_dict["src_payload"],
                   src_eff=metadata_dict["src_eff"],
                   src_ldts=metadata_dict["src_ldts"],
                   src_source=metadata_dict["src_source"],
                   source_model=metadata_dict["source_model"]) }}
