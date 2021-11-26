{{ config(
  materialized='incremental',
  schema = "SATS"
  ) }}

{%- set yaml_metadata -%}
source_model: 'stg_transactions_v1'
src_pk: 'PRODUCT_HK'
src_cdk:
  - "PRICE"
src_hashdiff: "PRODUCTS_HASHDIFF"
src_eff: "EFFECTIVE_FROM"
src_ldts: "LOAD_DATETIME"
src_source: "RECORD_SOURCE"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.ma_sat(src_pk=metadata_dict['src_pk'],
                   src_cdk=metadata_dict['src_cdk'],
                   src_payload=metadata_dict['src_payload'],
                   src_hashdiff=metadata_dict['src_hashdiff'],
                   src_eff=metadata_dict['src_eff'],
                   src_ldts=metadata_dict['src_ldts'],
                   src_source=metadata_dict['src_source'],
                   source_model=metadata_dict['source_model']) }}
