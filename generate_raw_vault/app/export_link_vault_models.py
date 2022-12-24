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
from json import dumps

LINK_TEMPLATE_PATH = "generate_raw_vault/app/templates/link_model.sql"
TRANS_LINK_TEMPLATE_PATH = "generate_raw_vault/app/templates/trans_link_model.sql"
NAME_DICTIONARY = "./name_dictionary.json"


def export_all_link_files(metadata_file_dirs):
    naming_dictionary = load_metadata_file(NAME_DICTIONARY)
    metadata_map = get_metadata_map(metadata_file_dirs)
    link_source_map = create_link_source_map(metadata_map)
    link_combinations = set(link_source_map.values())

    for link in link_combinations:
        substitution_values_template = create_substitution_values_template()
        for metadata_dict in metadata_map.values():
            link_substitution_values = populate_substitution_values(
                link, metadata_dict, substitution_values_template, naming_dictionary
            )

            if link_substitution_values:
                enriched_substitution_values = enrich_substitution_values(
                    link_substitution_values
                )
                substitutions = create_link_substitutions(enriched_substitution_values)
                if metadata_dict.get("transactional_payload"):
                    substitutions["model_type"] = "TRANS_LINKS"
                    model_template = fetch_template(TRANS_LINK_TEMPLATE_PATH)
                else:
                    substitutions["model_type"] = "LINKS"
                    model_template = fetch_template(LINK_TEMPLATE_PATH)

                write_model_files(
                    substitutions,
                    model_template,
                    filename=enriched_substitution_values["filename"],
                )


def create_link_substitutions(enriched_substitution_values):
    link_name = enriched_substitution_values.get("link_name")
    source_tables = enriched_substitution_values.get("source_tables")
    hash_key = enriched_substitution_values.get("hash_key")
    foreign_keys = enriched_substitution_values.get("foreign_keys")
    record_source = enriched_substitution_values.get("record_source")
    record_load_datetime = enriched_substitution_values.get("record_load_datetime")
    payload = enriched_substitution_values.get("payload")
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
    payload_columns = substitution_values.get("payload")
    substitution_values["hash_key"] = format_output_string(f"{link_name}_HK", 2)
    substitution_values["foreign_keys"] = f"\n".join(
        [format_output_string(f"{combination}_HK", 2) for combination in link_keys]
    )
    source_list.sort(reverse=True)
    if payload_columns:
        """There is a known bug for producing Transactional Links: regular Link tables
        are not versioned and can be feed by multiple staging tables, transactional links
        should be versioned and have a 1 to 1 mapping from versioned staging table to
        versioned transactional link table. The code below is a temporary fix which will
        take the most recent versioned staging table in the source list, it will not produce
        all versioned trans links currently"""
        substitution_values["source_tables"] = f'"stg_{source_list[0].lower()}"'
        substitution_values["payload"] = f"\n".join(
            [
                format_output_string(f"{payload_column}", 2)
                for payload_column in payload_columns
            ]
        )
    else:
        substitution_values["source_tables"] = f"\n".join(
            [format_output_string(f"stg_{source.lower()}", 2) for source in source_list]
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
                trans_payload_list = [
                    transaction_payload
                    for transaction_payload in metadata_dict.get(
                        "transactional_payload"
                    )
                ]
                substitution_values["payload"] = trans_payload_list
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


def fetch_template(model_path):
    model_template = load_template_file(model_path)
    template = Template(model_template)
    return template


def format_output_string(key, number_of_white_space):
    return f'{chr(32)*number_of_white_space}- "{key}"'


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    export_all_link_files(metadata_file_dirs)
