{{ config(
  materialized='incremental',
  schema = "SATS",
  alias = "store_iot_device_customer_visits_v0_1_0"
  ) }}

{%- set yaml_metadata -%}
source_model: "stg_customer_visits_v0_1_0"
src_pk: "CUSTOMER_HK"
src_hashdiff:
  source_column: "CUSTOMER_VISITS_HASHDIFF"
  alias: "HASHDIFF"
src_payload:
  - "TOTAL_VISITS"
src_eff: "EFFECTIVE_FROM"
src_ldts: "LOAD_DATETIME"
src_source: "RECORD_SOURCE"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.sat(src_pk=metadata_dict["src_pk"],
                src_hashdiff=metadata_dict["src_hashdiff"],
                src_payload=metadata_dict["src_payload"],
                src_eff=metadata_dict["src_eff"],
                src_ldts=metadata_dict["src_ldts"],
                src_source=metadata_dict["src_source"],
                source_model=metadata_dict["source_model"])   }}
