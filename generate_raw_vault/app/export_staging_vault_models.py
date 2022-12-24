from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.metadata_handler import Metadata
from generate_raw_vault.app.model_creation import create_set_from_list_of_lists
from string import Template

STAGING_TEMPLATE = "generate_raw_vault/app/templates/staging_model.sql"
SAT_HASHDIFF_TEMPLATE = "generate_raw_vault/app/templates/sat_hashdiff.sql"
NAME_DICTIONARY = "./name_dictionary.json"


def export_all_staging_files(metadata_file_dirs):
    for metadata_file_path in metadata_file_dirs:
        create_staging_file(metadata_file_path)


def create_staging_file(metadata_file_path):
    template = load_template_file(STAGING_TEMPLATE)
    staging_template = Template(template)

    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)
    hubs = metadata.get_hubs_from_business_topics()
    topics = metadata.get_business_topics()
    hub_substitutions_string = get_hub_substitutions_string(metadata, hubs)
    sat_substitutions_string = get_sat_substitutions_string(metadata, topics)
    unique_link_combinations_substitutions_string = (
        get_unique_link_combinations_substitutions_string(
            metadata, hubs, NAME_DICTIONARY
        )
    )
    hub_alias_substitutions_string = get_hub_alias_substitutions_string(metadata)
    substitutions = create_staging_subsitutions(
        metadata,
        hub_substitutions_string,
        hub_alias_substitutions_string,
        unique_link_combinations_substitutions_string,
        sat_substitutions_string,
    )
    staging_model = staging_template.substitute(substitutions)
    file_name = metadata.get_versioned_source_name().lower()
    with open(f"./models/raw_vault/stages/stg_{file_name}.sql", "w") as sql_export:
        sql_export.write(staging_model)


def get_hub_substitutions_string(metadata, hubs):
    hubs_substitutions = [hashkey_substitution(metadata, hub) for hub in hubs]
    return format_list_to_new_line_string(hubs_substitutions)


def format_list_to_new_line_string(input_list):
    return "\n".join(input_list)


def format_output_string(key, number_of_white_space):
    return f'{chr(32)*number_of_white_space}- "{key}"'


def format_hashkey_name(key, number_of_white_space):
    return f"{chr(32)*number_of_white_space}{key}"


def hashkey_substitution(metadata, hub):
    primary_keys = metadata.get_hub_business_key(hub)
    hub_hk = f"{hub}_HK:\n"
    format_hub_hk = format_hashkey_name(hub_hk, number_of_white_space=2)
    key_list = list(primary_keys.values())
    formatted_key_list = [
        format_output_string(key, number_of_white_space=4) for key in key_list
    ]
    primary_keys_list = format_list_to_new_line_string(formatted_key_list)
    hashkey_substitution = format_hub_hk + primary_keys_list
    return hashkey_substitution


def get_sat_substitutions_string(metadata, topics):
    sats_substitutions = [
        substitution
        for hub_name in topics
        if (substitution := get_sat_substitution_from_topic(metadata, hub_name))
        is not None
    ]
    return format_list_to_new_line_string(sats_substitutions)


def get_sat_substitution_from_topic(metadata, hub_name):
    template = load_template_file(SAT_HASHDIFF_TEMPLATE)
    sat_hashdiff_template = Template(template)
    satellites = metadata.get_sat_from_hub(hub_name)
    if satellites:
        sats = [
            get_sat_subs(sat_hashdiff_template, sat_name, payload)
            for sat_name, payload in satellites.items()
        ]
        return "\n".join(sats)


def get_sat_subs(sat_hashdiff_template, sat_name, payload):
    hashdiff = f"{sat_name}_HASHDIFF"
    if payload:
        sorted_payload_keys = sorted(payload.keys())
        formatted_sat_column_list = [f'- "{column}"' for column in sorted_payload_keys]
        formatted_sat_column_list_string = f"\n{chr(32)*6}".join(
            formatted_sat_column_list
        )
        substitutions = {
            "hashdiff_name": hashdiff,
            "columns": formatted_sat_column_list_string,
        }
        hashdiff_string = format_hashkey_name(
            sat_hashdiff_template.substitute(substitutions), number_of_white_space=2
        )
        return hashdiff_string


def get_unique_link_combinations_substitutions_string(
    metadata, hubs, naming_dictionary_path
):
    if len(hubs) > 1:
        naming_dictionary = load_metadata_file(naming_dictionary_path)
        for hub in hubs:
            if hub not in naming_dictionary:
                raise Exception(
                    f"Hub name missing from name dictionary, check hub name convention and existance in file {naming_dictionary_path}"
                )
        link_combination_string = "_".join([naming_dictionary[hub] for hub in hubs])
        unit_of_work = metadata.get_unit_of_work()
        link_name = f"{link_combination_string}_{unit_of_work}"
        combi_primary_keys = [
            list(metadata.get_hub_business_key(hub).values()) for hub in hubs
        ]
        unique_business_keys = sorted(create_set_from_list_of_lists(combi_primary_keys))
        link_keys = [
            format_output_string(business_key, number_of_white_space=4)
            for business_key in unique_business_keys
        ]
        formatted_primary_keys = format_list_to_new_line_string(link_keys)
        return f"  {link_name}_HK:\n{formatted_primary_keys}"
    else:
        return ""


def get_hub_alias_substitutions_string(metadata):
    hub_names_list = metadata.get_hubs_from_business_topics()
    alias_primary_key_association_list = []
    for hub_name in hub_names_list:
        alias_key_map = metadata.get_alias_key_map(
            metadata.get_hub_business_key(hub_name)
        )
        for alias, primary_key in alias_key_map.items():
            if alias != primary_key:
                alias_primary_key_association_list.append(
                    f'{alias}:{chr(32)}"{primary_key}"'
                )
    formatted_alias_primary_key_association_list = [
        format_hashkey_name(key_pair, number_of_white_space=2)
        for key_pair in alias_primary_key_association_list
    ]
    return format_list_to_new_line_string(formatted_alias_primary_key_association_list)


def create_staging_subsitutions(
    metadata,
    hubs_substitution,
    hub_alias_substitutions_string,
    unique_link_combinations_substitution,
    sat_substitution,
):
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    source_name = f"{database_name}_{schema_name}"
    table_name = metadata.get_versioned_source_name()

    derived_columns = [
        'EFFECTIVE_FROM: "LOAD_DATETIME"',
        'START_DATE: "LOAD_DATETIME"',
        '''END_DATE: "TO_TIMESTAMP_TZ('9999-01-01 00:00:00')"''',
    ]
    formatted_derived_columns = format_list_to_new_line_string(
        [
            format_hashkey_name(column, number_of_white_space=2)
            for column in derived_columns
        ]
    )

    substitutions = {
        "source": format_hashkey_name(
            f'{source_name}: "{table_name}"', number_of_white_space=2
        ),
        "derived_columns": formatted_derived_columns,
        "hashed_hubs_primary_key": hubs_substitution,
        "alias_columns": hub_alias_substitutions_string,
        "hashed_links": unique_link_combinations_substitution,
        "hashdiff": sat_substitution,
    }
    return substitutions


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    export_all_staging_files(metadata_file_dirs)
