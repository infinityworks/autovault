from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template
import itertools


def export_all_hub_files():
    aggregated_hubs = aggregate_hubs()
    for hub, substitutions in aggregated_hubs.items():
        template = load_template_file("generate_raw_vault/app/templates/hub_model.sql")
        hub_template = Template(template)
        hub_model = hub_template.substitute(substitutions)

        with open(f"./models/raw_vault/hubs/{hub.lower()}.sql", "w") as sql_export:
            sql_export.write(hub_model)


def aggregate_hubs():
    metadata_file_dirs = find_json_metadata("source_metadata")
    hubs = [get_hubs_from_file(file) for file in metadata_file_dirs]
    unique_hubs = set(list(itertools.chain(*hubs)))

    metadata_ = [
        Metadata(load_metadata_file(metadata_file_path))
        for metadata_file_path in metadata_file_dirs
    ]
    aggregated_hubs = {
        hub_name: substitution_template(hub_name) for hub_name in unique_hubs
    }
    for hub_name in unique_hubs:
        for metadata in metadata_:
            hub_int = metadata.get_business_topics()
            if hub_name in metadata.get_business_topics():
                hub_natural_key = metadata.get_hub_business_key(hub_name)
                aggregated_hubs[hub_name]["src_nk"] = hub_natural_key
                source_model = f"stg_{metadata.get_versioned_source_name().lower()}"
                aggregated_hubs[hub_name]["source_model"].append(f'"{source_model}"')
        format_aggregated_hub_sources(aggregated_hubs, hub_name)
    return aggregated_hubs


def get_hubs_from_file(metadata_file_path):
    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)
    hubs = metadata.get_hubs_from_business_topics()
    return hubs


def substitution_template(hub_name):
    hash_key = f"{hub_name}_HK"
    load_datetime = "LOAD_DATETIME"
    record_source = "RECORD_SOURCE"

    substitutions = {
        "source_model": [],
        "hub_name": hub_name,
        "src_pk": hash_key,
        "src_nk": "",
        "src_ldts": load_datetime,
        "src_source": record_source,
    }
    return substitutions


def format_aggregated_hub_sources(aggregated_hubs, hub_name):
    aggregated_hubs[hub_name]["source_model"] = f",\n{chr(32)*24}".join(
        aggregated_hubs[hub_name]["source_model"]
    )
    return aggregated_hubs


if __name__ == "__main__":
    export_all_hub_files()
