{{ config(
  materialized='incremental',
  schema = "TRANS_LINKS",
  alias = "CUST_PRDCT_STORE_CHECKOUT"
  ) }}

{%- set yaml_metadata -%}
source_model: "stg_transactions_v0_2_0"
src_pk:
  - "CUST_PRDCT_STORE_CHECKOUT_HK"
src_fk:
  - "CUSTOMER_HK"
  - "PRODUCT_HK"
src_payload:
  - "DATE_OF_SESSION"
src_eff: "EFFECTIVE_FROM"
src_ldts: "LOAD_DATETIME"
src_source: "RECORD_SOURCE"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ dbtvault.t_link(src_pk=metadata_dict["src_pk"],
                   src_fk=metadata_dict["src_fk"],
                   src_payload=metadata_dict["src_payload"],
                   src_eff=metadata_dict["src_eff"],
                   src_ldts=metadata_dict["src_ldts"],
                   src_source=metadata_dict["src_source"],
                   source_model=metadata_dict["source_model"]) }}
