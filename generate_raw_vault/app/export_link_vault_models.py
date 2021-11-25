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

    file_map = get_file_map(metadata_file_dirs)
    link_source_map = create_hub_source_map(file_map)
    link_combinations = set(
        [
            f'{descriptors["link"]}_{descriptors["unit_of_work"]}'
            for descriptors in link_source_map.values()
        ]
    )
    #  include UoW
    for link_combination in link_combinations:
        create_link_model_files(
            file_map,
            link_source_map,
            link_combination,
            link_template,
            naming_dictionary,
        )


def create_link_model_files(
    file_map, link_source_map, link_combination, link_template, naming_dictionary
):
    source_list = [
        descriptors["source_name"]
        for descriptors in link_source_map.values()
        if f'{descriptors["link"]}_{descriptors["unit_of_work"]}' == link_combination
    ]
    # print(source_list)
    link_keys = link_combination.split("_")
    print(link_keys)
    # short name to include UoW A_B_C_UoW
    # create short name and concat UoW
    # short_name = "_".join([naming_dictionary[key] for key in link_keys])
    # file_name = short_name.lower()

    # substitutions = create_link_substitutions(source_list, link_keys, short_name)
    # link_model = link_template.substitute(substitutions)
    # with open(f"./models/raw_vault/links/{file_name}.sql", "w") as sql_export:
    #     sql_export.write(link_model)


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


def get_file_map(metadata_file_dirs):
    file_map = {
        str(file_path): load_metadata_file(file_path)
        for file_path in metadata_file_dirs
    }
    return file_map


def create_hub_source_map(file_map):
    metadata_files = file_map.values()
    hub_source_map = {
        file_path: {
            "source_name": list(get_map_of_source_and_hubs(metadata).keys())[0],
            "link": "_".join(list(get_map_of_source_and_hubs(metadata).values())[0]),
            "unit_of_work": metadata.get("unit_of_work"),
        }
        for file_path, metadata in file_map.items()
        if len(list(get_map_of_source_and_hubs(metadata).values())[0]) > 1
    }
    return hub_source_map


def get_map_of_source_and_hubs(metadata):
    read_metadata = Metadata(metadata)
    hubs = read_metadata.get_hubs_from_business_topics()
    return {read_metadata.get_versioned_source_name(): hubs}


if __name__ == "__main__":
    export_all_link_files()
