from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template
import json
import itertools
from pathlib import Path


def export_all_link_files():
    metadata_file_dirs = find_json_metadata("source_metadata")
    all_files_unique_link_combinations = get_allfiles_unique_link_combinations(
        metadata_file_dirs
    )
    create_link_model_files(all_files_unique_link_combinations, metadata_file_dirs)


def get_allfiles_unique_link_combinations(metadata_file_dirs):

    all_files_link_combinations = []
    for metadata_file_path in metadata_file_dirs:

        metadata_file = load_metadata_file(metadata_file_path)
        metadata = Metadata(metadata_file)
        hubs = metadata.get_hubs_from_business_topics()
        unique_link_combis = itertools.combinations(sorted(hubs), 2)
        for link_combi in unique_link_combis:
            all_files_link_combinations.append(link_combi)

    return list(set(all_files_link_combinations))


def create_link_model_files(all_files_link_combinations, metadata_file_dirs):

    template = load_template_file("generate_raw_vault/app/templates/link_model.sql")
    link_template = Template(template)

    for link_combi in all_files_link_combinations:
        source_list = []
        for metadata_file_path in metadata_file_dirs:
            metadata_file = load_metadata_file(metadata_file_path)
            metadata = Metadata(metadata_file)
            hubs = metadata.get_hubs_from_business_topics()
            if set((link_combi)).issubset(hubs) == True:
                source_list.append(metadata.get_versioned_source_name())
        file_name = f'{"_".join(link_combi)}'.lower()
        substitutions = create_link_subsitutions(source_list, file_name, link_combi)
        link_model = link_template.substitute(substitutions)
        with open(f"./models/raw_vault/links/{file_name}.sql", "w") as sql_export:
            sql_export.write(link_model)


def create_link_subsitutions(source_list, file_name, link_combi):

    table_name = json.dumps(list(map(lambda source: "stg_" + source, source_list)))
    hash_key = (file_name + "_HK").upper()
    src_fk = json.dumps(list(map(lambda combi: combi + "_HK", link_combi)))
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
