from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.metadata_handler import Metadata
from generate_raw_vault.app.model_creation import create_set_from_list_of_lists
from string import Template
from typing import Set, Any
from generate_raw_vault.app.model_creation import (
    create_substitution_values_template,
    write_model_files,
)

HUB_TEMPLATE = "generate_raw_vault/app/templates/hub_model.sql"


def export_all_hub_files(metadata_file_dirs):
    template = load_template_file(HUB_TEMPLATE)
    hub_template = Template(template)
    all_metadata = {
        str(metadata_file_path): Metadata(load_metadata_file(metadata_file_path))
        for metadata_file_path in metadata_file_dirs
    }
    list_of_hub_lists_per_metadata_file = get_list_of_hub_lists(all_metadata)
    unique_hubs = create_set_from_list_of_lists(list_of_hub_lists_per_metadata_file)
    substitution_values = create_substitution_values_template()
    hub_substitutions = create_hub_substitution_template(substitution_values)
    for hub_name in unique_hubs:
        substitutions = populate_hub_substitutions(
            hub_name, hub_substitutions, all_metadata
        )
        if substitutions.get("source_list"):
            substitutions["model_type"] = "HUBS"
            formatted_hub_name = hub_name.lower()
            write_model_files(
                substitutions,
                hub_template,
                formatted_hub_name,
            )


def populate_hub_substitutions(hub_name, hub_substitutions, all_metadata):
    natural_key_list = []
    source_list = []
    for metadata in all_metadata.values():
        if hub_name in metadata.get_business_topics():
            natural_key_list = populate_hub_natural_key(
                natural_key_list, metadata, hub_name
            )
            discard_source_from_source_list = (
                metadata.check_ignore_source_from_hub_model(hub_name)
            )
            if discard_source_from_source_list:
                continue
            source_list = get_hub_source_list(metadata, source_list)

    hub_natural_key_set = set(create_set_from_list_of_lists(natural_key_list))
    formatted_hub_natural_key_set = format_string_list_with_double_quotes(
        list(hub_natural_key_set)
    )
    natural_key_substitution = format_list_ouput_with_newlines(
        formatted_hub_natural_key_set, white_space=18
    )

    substitutions = {
        "hub_name": hub_name,
        "source_list": format_list_ouput_with_newlines(source_list),
        "src_nk": natural_key_substitution,
        "src_pk": f"{hub_name}_HK",
        "src_ldts": hub_substitutions["src_ldts"],
        "src_source": hub_substitutions["src_source"],
    }
    return substitutions


def populate_hub_natural_key(natural_key_list, metadata, hub_name):
    hub_natural_key = metadata.get_hub_business_key(hub_name)
    natural_key_list.append(list(hub_natural_key.values()))
    return natural_key_list


def get_hub_source_list(metadata, source_list):
    source_name = get_formatted_source_name(metadata)
    source_list.append(source_name)
    return source_list


def format_string_list_with_double_quotes(input_list):
    formatted_list = [f'"{input_string}"' for input_string in input_list]
    return formatted_list


def format_list_ouput_with_newlines(source_list, white_space=24):
    return f",\n{chr(32)*white_space}".join(sorted(source_list))


def get_formatted_source_name(metadata):
    return f'"stg_{metadata.get_versioned_source_name().lower()}"'


def get_list_of_hub_lists(all_metadata):
    return [
        metadata.get_hubs_from_business_topics() for metadata in all_metadata.values()
    ]


def create_hub_substitution_template(substitution_values):
    substitutions = {
        "source_list": substitution_values["source_list"],
        "hub_name": substitution_values["hub_name"],
        "src_pk": substitution_values["hash_key"],
        "src_nk": substitution_values["natural_key"],
        "src_ldts": substitution_values["record_load_datetime"],
        "src_source": substitution_values["record_source"],
    }
    return substitutions


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    export_all_hub_files(metadata_file_dirs)
