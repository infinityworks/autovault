from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.metadata_handler import Metadata
from string import Template
import json
from itertools import combinations, chain

LINK_TEMPLATE_PATH = "generate_raw_vault/app/templates/link_model.sql"
NAME_DICTIONARY = "./name_dictionary.json"


def export_all_link_files():
    template = load_template_file(LINK_TEMPLATE_PATH)
    naming_dictionary = load_metadata_file(NAME_DICTIONARY)
    link_template = Template(template)
    metadata_file_dirs = find_json_metadata("source_metadata")
    hub_source_map = create_hub_source_map(metadata_file_dirs)
    link_source_map = concatinate_hubs_to_link(hub_source_map)
    link_combinations = set(link_source_map.values())
    for link_combination in link_combinations:
        create_link_model_files(
            link_source_map, link_combination, link_template, naming_dictionary
        )


def concatinate_hubs_to_link(hub_source_map):
    link_map = {source: "_".join(hubs) for source, hubs in hub_source_map.items()}
    return link_map


def create_hub_source_map(metadata_file_dirs):
    hub_source_map = {
        list(get_map_of_source_and_hubs(metadata_file_path).keys())[0]: list(
            get_map_of_source_and_hubs(metadata_file_path).values()
        )[0]
        for metadata_file_path in metadata_file_dirs
        if len(list(get_map_of_source_and_hubs(metadata_file_path).values())[0]) > 1
    }
    return hub_source_map


def get_map_of_source_and_hubs(metadata_file_path):
    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)
    hubs = metadata.get_hubs_from_business_topics()
    return {metadata.get_versioned_source_name(): hubs}


def create_link_model_files(
    link_source_map, link_combination, link_template, naming_dictionary
):
    source_list = [
        source_name
        for source_name, link in link_source_map.items()
        if link == link_combination
    ]
    link_keys = link_combination.split("_")
    short_name = "_".join([naming_dictionary[key] for key in link_keys])
    file_name = short_name.lower()

    substitutions = create_link_substitutions(source_list, link_keys, short_name)
    link_model = link_template.substitute(substitutions)
    with open(f"./models/raw_vault/links/{file_name}.sql", "w") as sql_export:
        sql_export.write(link_model)


def create_link_substitutions(source_list, link_keys, short_name):
    table_name = f",\n{chr(32)*24}".join(
        [f'"stg_{source.lower()}"' for source in source_list]
    )
    hash_key = (short_name + "_HK").upper()
    src_fk = f",\n{chr(32)*18}".join(
        [f'"{combination}_HK"' for combination in link_keys]
    )
    load_datetime = "LOAD_DATETIME"
    record_source = "RECORD_SOURCE"
    substitutions = {
        "source_model": table_name,
        "src_pk": hash_key,
        "src_fk": src_fk,
        "src_ldts": load_datetime,
        "src_source": record_source,
    }

    return substitutions


if __name__ == "__main__":
    export_all_link_files()
