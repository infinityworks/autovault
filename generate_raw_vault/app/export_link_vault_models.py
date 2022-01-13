from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.metadata_handler import Metadata
from string import Template

LINK_TEMPLATE_PATH = "generate_raw_vault/app/templates/link_model.sql"
NAME_DICTIONARY = "./name_dictionary.json"


def export_all_link_files():
    template = load_template_file(LINK_TEMPLATE_PATH)
    naming_dictionary = load_metadata_file(NAME_DICTIONARY)
    link_template = Template(template)
    metadata_file_dirs = find_json_metadata("source_metadata")

    metadata_map = get_metadata_map(metadata_file_dirs)
    link_source_map = create_link_source_map(metadata_map)
    link_combinations = set(link_source_map.values())

    for link in link_combinations:
        substitution_values_template = create_substitution_values_template()
        for metadata_dict in metadata_map.values():
            substitution_values = create_substitution_values(
                link, metadata_dict, substitution_values_template, naming_dictionary
            )
            if substitution_values:
                link_substitutions = create_link_substitutions(substitution_values)
                create_link_model_files(
                    link_substitutions, link_template, substitution_values["filename"]
                )


def create_link_model_files(substitutions, link_template, filename):
    link_model = link_template.substitute(substitutions)
    with open(f"./models/raw_vault/links/{filename}.sql", "w") as sql_export:
        sql_export.write(link_model)


def create_link_substitutions(substitution_values):
    source_list = substitution_values["source_list"]
    link_keys = substitution_values["hubs"]
    link_name = substitution_values["link_name"]

    source_tables = f",\n{chr(32)*24}".join(
        [f'"stg_{source.lower()}"' for source in source_list]
    )
    hash_key = (link_name + "_HK").upper()
    src_fk = f",\n{chr(32)*18}".join(
        [f'"{combination}_HK"' for combination in link_keys]
    )
    load_datetime = "LOAD_DATETIME"
    record_source = "RECORD_SOURCE"
    substitutions = {
        "alias": link_name,
        "source_model": source_tables,
        "src_pk": hash_key,
        "src_fk": src_fk,
        "src_ldts": load_datetime,
        "src_source": record_source,
    }

    return substitutions


def create_substitution_values(
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
            filename = f'{"_".join(hub_list)}_{unit_of_work}'.lower()
            substitution_values["hubs"] = hub_list
            substitution_values["filename"] = filename
            substitution_values["link_name"] = link_name
            substitution_values["source_list"].append(versioned_source_name)
            return substitution_values


def create_substitution_values_template():
    return {
        "hubs": "",
        "filename": "",
        "link_name": "",
        "source_list": [],
    }


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


if __name__ == "__main__":
    export_all_link_files()
