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
    unique_hubs = get_unique_hubs(list_of_hub_lists_per_metadata_file)
    substitution_values = create_substitution_values_template()
    hub_substitutions = create_hub_substitution_template(substitution_values)
    for hub_name in unique_hubs:
        substitutions = populate_hub_substitutions(
            hub_name, hub_substitutions, all_metadata
        )
        formatted_hub_name = format_hub_name(hub_name)
        write_model_files(substitutions, hub_template, "hubs", formatted_hub_name)


def populate_hub_substitutions(hub_name, hub_substitutions, all_metadata):
    natural_key_list = []
    source_list = []
    for metadata in all_metadata.values():
        if hub_name in metadata.get_business_topics():
            natural_key_list = populate_hub_natural_key(
                natural_key_list, metadata, hub_name
            )
            source_list = get_hub_source_list(metadata, source_list)

    substitutions = {
        "hub_name": hub_name,
        "source_list": format_sources_list(source_list),
        "src_nk": natural_key_list[0],
        "src_pk": f"{hub_name}_HK",
        "src_ldts": hub_substitutions["src_ldts"],
        "src_source": hub_substitutions["src_source"],
    }
    return substitutions


def populate_hub_natural_key(natural_key_list, metadata, hub_name):
    hub_natural_key = metadata.get_hub_business_key(hub_name)
    natural_key_list.append(hub_natural_key)
    natural_key_set = set(natural_key_list)
    if len(natural_key_set) > 1:
        raise Exception(
            f"Multiple natural keys found for hub {hub_name}, check metadata files that they are standardised or correctly aliased."
        )
    return natural_key_list


def get_hub_source_list(metadata, source_list):
    source_name = get_formatted_source_name(metadata)
    source_list.append(source_name)
    return source_list


def format_hub_name(hub_name):
    return f"{hub_name.lower()}_hub"


def format_sources_list(source_list):
    return f",\n{chr(32)*24}".join(sorted(source_list))


def get_formatted_source_name(metadata):
    return f'"stg_{metadata.get_versioned_source_name().lower()}"'


def get_aggregated_hubs(unique_hubs: Set[str]):
    return {hub_name: substitution_template(hub_name) for hub_name in unique_hubs}


def get_unique_hubs(hubs) -> Set[str]:
    return set(list(itertools.chain(*hubs)))


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
