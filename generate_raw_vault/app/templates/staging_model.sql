{%- set yaml_metadata -%}
source_model:
  $source
derived_columns:
  $derived_columns
hashed_columns:
  $hashed_primary_key
  $hashdiff
    is_hashdiff: true
    columns:
      $columns
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.stage(include_source_columns=true,
                  source_model=metadata_dict['source_model'],
                  derived_columns=metadata_dict['derived_columns'],
                  hashed_columns=metadata_dict['hashed_columns'],
                  ranked_columns=none) }}
