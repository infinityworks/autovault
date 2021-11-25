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
    link_source_map = create_link_source_map(file_map)
    link_combinations = set(link_source_map.values())
    for link in link_combinations:
        source_list = []
        for file_path, metadata in file_map.items():
            hub_list = Metadata(metadata).get_hubs_from_business_topics()
            if len(hub_list) > 1:
                linked_hubs = "_".join(hub_list)
                unit_of_work = metadata.get("unit_of_work")
                if f"{linked_hubs}_{unit_of_work}" == link:
                    source_list.append(Metadata(metadata).get_versioned_source_name())
                    short_name = "_".join([naming_dictionary[hub] for hub in hub_list])
                    name = f"{short_name}_{unit_of_work}"
                    substitution_values = {"hubs": hub_list, "file_name": name.lower()}
        substitution_values.update({"source_list": sorted(source_list)})
        substitutions = create_link_substitutions(substitution_values)
        create_link_model_files(
            substitutions, link_template, substitution_values["file_name"]
        )

    #  use the full hub names for the filename to void duplicate files generated if naming dictionary changes
    #  update link template to to include an alias to use shorterned naming for tablename


def create_link_model_files(substitutions, link_template, file_name):
    link_model = link_template.substitute(substitutions)
    with open(f"./models/raw_vault/links/{file_name}.sql", "w") as sql_export:
        sql_export.write(link_model)


def create_link_substitutions(substitution_values):
    source_list = substitution_values["source_list"]
    link_keys = substitution_values["hubs"]
    short_name = substitution_values["file_name"]

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


def create_link_source_map(file_map):
    metadata_files = file_map.values()
    link_source_map = {
        file_path: f'{"_".join(list(get_map_of_source_and_hubs(metadata).values())[0])}_{metadata.get("unit_of_work")}'
        for file_path, metadata in file_map.items()
        if len(list(get_map_of_source_and_hubs(metadata).values())[0]) > 1
    }
    return link_source_map


def get_map_of_source_and_hubs(metadata):
    read_metadata = Metadata(metadata)
    hubs = read_metadata.get_hubs_from_business_topics()
    return {read_metadata.get_versioned_source_name(): hubs}


if __name__ == "__main__":
    export_all_link_files()
