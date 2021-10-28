from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template
import json
import itertools

STAGING_TEMPLATE = "generate_raw_vault/app/templates/staging_model.txt"


def export_all_staging_files():
    metadata_file_dirs = find_json_metadata("source_metadata")
    for metadata_file_path in metadata_file_dirs:
        create_staging_file(metadata_file_path)


def create_staging_file(metadata_file_path):
    template = load_template_file(STAGING_TEMPLATE)
    staging_template = Template(template)

    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)

    hubs = metadata.get_hubs_from_business_topics()
    topics = metadata.get_business_topics()
    unique_link_combis = itertools.combinations(sorted(hubs), 2)

    hub_substitutions_string = get_hub_substitutions_string(metadata, hubs)
    sat_substitutions_string = get_sat_substitutions_string(topics)
    unique_link_combis_substitutions_string = get_unique_link_combis_substitutions_string(
        metadata, unique_link_combis
    )

    substitutions = create_staging_subsitutions(
        metadata,
        hub_substitutions_string,
        unique_link_combis_substitutions_string,
        sat_substitutions_string,
    )
    staging_model = staging_template.substitute(substitutions)
    file_name = metadata.get_versioned_source_name().lower()
    with open(f"./models/raw_vault/stages/stg_{file_name}.sql", "w") as sql_export:
        sql_export.write(staging_model)


def format_derived_columns(column_list):
    return "\n  ".join(column_list)


def create_substitutions_string(substitutions):
    substitutions_string = "\n  ".join(substitutions)
    return substitutions_string


def get_hub_substitutions_string(metadata, hubs):
    hubs_substitutions = []
    for hub in hubs:
        primary_key = metadata.get_hub_business_key(hub)
        hubs_substitutions.append(f'{hub}_HK: "{primary_key}"')
    return create_substitutions_string(hubs_substitutions)


def get_sat_substitutions_string(topics):
    sats_substitutions = []
    for topic in topics:
        hub = f'"{topic}"'
        hashdiff = f"{topic}_HASHDIFF"
        sat_payload_columns_list = list(
            topics[topic].get("business_attributes")[0].get("payload").keys()
        )
        formatted_sat_column_list = list(
            map(lambda column: "- " + f'"{column}"', sat_payload_columns_list)
        )
        formatted_sat_column_list_string = "\n.   ".join(formatted_sat_column_list)
        sat_string = (
            hashdiff
            + ":\n"
            + "   is_hashdiff: true\n"
            + "   columns:"
            + "\n    "
            + formatted_sat_column_list_string
        )
        sats_substitutions.append(sat_string)
    return create_substitutions_string(sats_substitutions)


def get_unique_link_combis_substitutions_string(metadata, unique_link_combis):
    unique_link_combis_substitutions = []
    for unique_link_combi in unique_link_combis:
        link_join = "_".join(unique_link_combi)
        combi_primary_keys = []
        for hub_in_combi in unique_link_combi:
            each_primary_key = metadata.get_hub_business_key(hub_in_combi)
            combi_primary_keys.append(f'- "{each_primary_key}"')
        primarykeys_join = "\n   ".join(combi_primary_keys)
        unique_link_combis_substitutions.append(
            f"{link_join}_HK:\n   {primarykeys_join}"
        )
    return create_substitutions_string(unique_link_combis_substitutions)


def create_staging_subsitutions(
    metadata, hubs_substitution, unique_link_combis_substitution, sat_substitution
):
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    source_name = f"{database_name}_{schema_name}"
    table_name = metadata.get_versioned_source_name()

    derived_columns = [
        'EFFECTIVE_FROM: "LOAD_DATETIME"',
        'START_DATE: "LOAD_DATETIME"',
        '''END_DATE: "TO_DATE('9999-12-31')"''',
    ]
    formatted_derived_columns = format_derived_columns(derived_columns)

    substitutions = {
        "source": f'{source_name}: "{table_name}"',
        "derived_columns": formatted_derived_columns,
        "hashed_hubs_primary_key": hubs_substitution,
        "hashed_links": unique_link_combis_substitution,
        "hashdiff": sat_substitution,
    }
    return substitutions


if __name__ == "__main__":
    export_all_staging_files()
