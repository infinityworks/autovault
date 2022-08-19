from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.model_creation import (
    create_substitution_values_template,
    write_model_files,
)
from generate_raw_vault.app.metadata_handler import Metadata
from string import Template
import itertools

LINK_TEMPLATE_PATH = "generate_raw_vault/app/templates/link_model.sql"
TRANS_LINK_TEMPLATE_PATH = "generate_raw_vault/app/templates/trans_link_model.sql"
NAME_DICTIONARY = "./name_dictionary.json"


def export_all_link_files(metadata_file_dirs):
    template = load_template_file(LINK_TEMPLATE_PATH)
    translink_template = load_template_file(TRANS_LINK_TEMPLATE_PATH)
    naming_dictionary = load_metadata_file(NAME_DICTIONARY)
    translink_template = Template(translink_template)
    link_template = Template(template)
    templates = {"link": link_template, "trans_link": translink_template}
    metadata_map = get_metadata_map(metadata_file_dirs)
    link_source_map = create_link_source_map(metadata_map)
    link_combinations = set(link_source_map.values())

    for link in link_combinations:
        substitution_values_template = create_substitution_values_template()
        for metadata_dict in metadata_map.values():
            if metadata_dict.get("transactional_payload"):
                model_template = templates.get("trans_link")
            else:
                model_template = templates.get("link")
            substitution_values = populate_substitution_values(
                link, metadata_dict, substitution_values_template, naming_dictionary
            )
            if substitution_values:
                enriched_substitution_values = enrich_substitution_values(
                    substitution_values
                )
                substitutions = create_link_substitutions(enriched_substitution_values)
                write_model_files(
                    substitutions,
                    model_template,
                    model_type="link",
                    filename=enriched_substitution_values["filename"],
                )


def create_link_substitutions(enriched_substitution_values):
    link_name = enriched_substitution_values["link_name"]
    source_tables = enriched_substitution_values["source_tables"]
    hash_key = enriched_substitution_values["hash_key"]
    foreign_keys = enriched_substitution_values["foreign_keys"]
    record_source = enriched_substitution_values["record_source"]
    record_load_datetime = enriched_substitution_values["record_load_datetime"]
    payload = enriched_substitution_values["payload"]
    substitutions = {
        "alias": link_name,
        "source_model": source_tables,
        "src_pk": hash_key,
        "src_fk": foreign_keys,
        "payload": payload,
        "src_ldts": record_load_datetime,
        "src_source": record_source,
    }
    return substitutions


def enrich_substitution_values(substitution_values):
    source_list = substitution_values["source_list"]
    link_keys = substitution_values["hubs"]
    link_name = substitution_values["link_name"]
    payload_columns = substitution_values["payload"]
    substitution_values["source_tables"] = f",\n{chr(32)*24}".join(
        sorted([f'"stg_{source.lower()}"' for source in source_list])
    )
    substitution_values["hash_key"] = (link_name + "_HK").upper()
    if payload_columns is None:
        substitution_values["foreign_keys"] = f",\n{chr(32)*18}".join(
            [f'"{combination}_HK"' for combination in link_keys]
        )
    else:
        substitution_values["foreign_keys"] = f"\n".join(
            [format_output_string(f"{combination}_HK", 4) for combination in link_keys]
        )
        substitution_values["payload"] = f"\n".join(
            [
                format_output_string(f"{payload_column}", 4)
                for payload_column in payload_columns
            ]
        )
    return substitution_values


def populate_substitution_values(
    link, metadata_dict, substitution_values, naming_dictionary
):
    metadata = Metadata(metadata_dict)
    hub_list = metadata.get_hubs_from_business_topics()
    if len(hub_list) > 1:
        linked_hubs = "_".join(hub_list)
        unit_of_work = metadata.get_unit_of_work()
        if f"{linked_hubs}_{unit_of_work}" == link:
            filename = f'{"_".join(hub_list)}_{unit_of_work}'.lower()
            short_name = "_".join(
                [
                    naming_dictionary[hub] if hub in naming_dictionary else hub
                    for hub in hub_list
                ]
            )
            link_name = f"{short_name}_{unit_of_work}"
            versioned_source_name = metadata.get_versioned_source_name()
            substitution_values["hubs"] = hub_list
            substitution_values["filename"] = filename
            substitution_values["link_name"] = link_name
            substitution_values["source_list"].append(versioned_source_name)
            if metadata_dict.get("transactional_payload"):
                trans_payload_list = []
                for transaction_payload in metadata_dict.get("transactional_payload"):
                    trans_payload_list.append(transaction_payload)
                substitution_values["payload"] = trans_payload_list
            else:
                substitution_values["payload"] = None
            return substitution_values


def create_link_source_map(metadata_map):
    link_source_map = {
        file_path: f'{"_".join(list(get_map_of_source_and_hubs(metadata).values())[0])}_{Metadata(metadata).get_unit_of_work()}'
        for file_path, metadata in metadata_map.items()
        if len(list(get_map_of_source_and_hubs(metadata).values())[0]) > 1
    }
    return link_source_map


def get_map_of_source_and_hubs(metadata):
    read_metadata = Metadata(metadata)
    hubs = read_metadata.get_hubs_from_business_topics()
    return {read_metadata.get_versioned_source_name(): hubs}


def get_metadata_map(metadata_file_dirs):
    metadata_map = {
        str(file_path): load_metadata_file(file_path)
        for file_path in metadata_file_dirs
    }
    return metadata_map


def format_output_string(key, number_of_white_space):
    return f"{chr(32)*number_of_white_space}- '{key}'"


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    export_all_link_files(metadata_file_dirs)
