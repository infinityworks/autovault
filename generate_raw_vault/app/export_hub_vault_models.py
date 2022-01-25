from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.metadata_handler import Metadata
from string import Template
import itertools
from typing import Set, Any
from generate_raw_vault.app.model_creation import (
    create_substitution_values_template,
    write_model_files,
)
import json

HUB_TEMPLATE = "generate_raw_vault/app/templates/hub_model.sql"


def export_all_hub_files(metadata_file_dirs):
    aggregated_hub_substitutions = aggregate_hubs(metadata_file_dirs)
    template = load_template_file(HUB_TEMPLATE)
    hub_template = Template(template)
    for hub, substitutions in aggregated_hub_substitutions.items():
        hub_name = f"{hub.lower()}_hub"
        write_model_files(substitutions, hub_template, "hubs", hub_name)


def aggregate_hubs(metadata_file_dirs):
    hubs = [get_hubs_from_file(file) for file in metadata_file_dirs]
    unique_hubs = get_unique_hubs(hubs)
    all_metadata = {
        str(metadata_file_path): Metadata(load_metadata_file(metadata_file_path))
        for metadata_file_path in metadata_file_dirs
    }
    substitution_values = create_substitution_values_template()
    for hub_name in unique_hubs:
        aggregated_hubs = get_aggregated_hubs(substitution_values, unique_hubs)
        for metadata in all_metadata.values():
            if hub_name in list(metadata.get_business_topics().keys()):
                hub_natural_key = metadata.get_hub_business_key(hub_name)
                aggregated_hubs[hub_name]["src_nk"] = hub_natural_key
                source_name = f'"stg_{metadata.get_versioned_source_name().lower()}"'
                # print(hub_name, source_name)
                # print(aggregated_hubs[hub_name]["source_list"])
                aggregated_hubs[hub_name]["source_list"].append(source_name)
        format_aggregated_hub_sources(aggregated_hubs, hub_name)
    # print(json.dumps(aggregated_hubs, indent=2))
    # print(aggregated_hubs)
    return aggregated_hubs


def get_hubs_from_file(metadata_file_path):
    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)
    hubs = metadata.get_hubs_from_business_topics()
    return hubs


def create_hub_substitution(substitution_values, hub_name):
    substitution_values["hash_key"] = f"{hub_name}_HK"

    substitutions = {
        "source_list": substitution_values["source_list"],
        "hub_name": hub_name,
        "src_pk": substitution_values["hash_key"],
        "src_nk": "",
        "src_ldts": substitution_values["record_load_datetime"],
        "src_source": substitution_values["record_source"],
    }
    return substitutions


def get_unique_hubs(hubs) -> Set[str]:
    return sorted(set(list(itertools.chain(*hubs))))


def get_aggregated_hubs(substitution_values, unique_hubs: Set[str]):
    return {
        hub_name: create_hub_substitution(substitution_values, hub_name)
        for hub_name in unique_hubs
    }


def format_aggregated_hub_sources(aggregated_hubs, hub_name):
    aggregated_hubs[hub_name]["source_list"] = f",\n{chr(32)*24}".join(
        sorted(aggregated_hubs[hub_name]["source_list"])
    )
    return aggregated_hubs


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    export_all_hub_files(metadata_file_dirs)
