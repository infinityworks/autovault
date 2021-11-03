from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template
import json
import itertools

HUB_TEMPLATE_PATH = "generate_raw_vault/app/templates/link_model.sql"


def export_all_link_files():
    template = load_template_file(HUB_TEMPLATE_PATH)
    link_template = Template(template)
    metadata_file_dirs = find_json_metadata("source_metadata")
    all_unique_link_combinations = get_all_unique_link_combinations(metadata_file_dirs)
    hub_source_map = create_hub_source_map(metadata_file_dirs)
    for link_combination in all_unique_link_combinations:
        create_link_model_files(link_combination, link_template, hub_source_map)


def get_all_unique_link_combinations(metadata_file_dirs):
    hubs = get_hubs_from_metadata_files(metadata_file_dirs)
    link_combinations = [list(itertools.combinations(sorted(hub), 2)) for hub in hubs]
    all_files_link_combinations = set(list(itertools.chain(*link_combinations)))
    return all_files_link_combinations


def get_hubs_from_metadata_files(metadata_file_dirs):
    hubs = [
        Metadata(load_metadata_file(file_path)).get_hubs_from_business_topics()
        for file_path in metadata_file_dirs
    ]
    return hubs


def create_hub_source_map(metadata_file_dirs):
    hub_source_map = {
        list(get_map_of_source_and_hubs(metadata_file_path).keys())[0]: list(
            get_map_of_source_and_hubs(metadata_file_path).values()
        )[0]
        for metadata_file_path in metadata_file_dirs
    }
    return hub_source_map


def get_map_of_source_and_hubs(metadata_file_path):
    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)
    hubs = metadata.get_hubs_from_business_topics()
    return {metadata.get_versioned_source_name(): hubs}


def create_link_model_files(link_combination, link_template, hub_source_map):
    source_list = [
        source_name
        for source_name, hubs in hub_source_map.items()
        if set(link_combination).issubset(hubs)
    ]
    file_name = f'{"_".join(link_combination)}'.lower()
    substitutions = create_link_subsitutions(source_list, file_name, link_combination)
    link_model = link_template.substitute(substitutions)
    with open(f"./models/raw_vault/links/{file_name}_link.sql", "w") as sql_export:
        sql_export.write(link_model)


def create_link_subsitutions(source_list, file_name, link_combination):

    table_name = json.dumps(list(map(lambda source: "stg_" + source, source_list)))
    table_name = f",\n{chr(32)*24}".join(
        [f'"stg_{source.lower()}"' for source in source_list]
    )
    hash_key = (file_name + "_HK").upper()
    src_fk = json.dumps(list(map(lambda combi: combi + "_HK", link_combination)))
    src_fk = f",\n{chr(32)*18}".join(
        [f'"{combination}_HK"' for combination in link_combination]
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
