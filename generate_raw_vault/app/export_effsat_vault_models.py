from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.metadata_handler import Metadata
from generate_raw_vault.app.model_creation import write_model_files
from string import Template


EFF_SAT_TEMPLATE_PATH = "generate_raw_vault/app/templates/effect_sat_model.sql"
NAME_DICTIONARY = "./name_dictionary.json"


def export_all_effsat_files(metadata_file_dirs):
    template = load_template_file(EFF_SAT_TEMPLATE_PATH)
    naming_dictionary = load_metadata_file(NAME_DICTIONARY)
    link_template = Template(template)
    file_map = get_file_map(metadata_file_dirs)
    link_source_map = create_link_source_map(file_map)
    link_combinations = set(link_source_map.values())

    for link in link_combinations:
        for metadata_dict in file_map.values():
            metadata = Metadata(metadata_dict)
            hub_list = metadata.get_hubs_from_business_topics()
            linked_hubs = "_".join(hub_list)
            unit_of_work = metadata.get_unit_of_work()
            if f"{linked_hubs}_{unit_of_work}" == link:
                source = metadata.get_versioned_source_name()
                short_name = "_".join([naming_dictionary[hub] for hub in hub_list])
                name = f"{short_name}_{unit_of_work}_v{metadata.get_source_version()}"
                link_key = f"{short_name}_{unit_of_work}"
                substitution_values = {"hubs": hub_list, "file_name": name.lower()}
                substitution_values.update({"source": source})
                substitution_values.update({"link_key": link_key})
                substitution_values.update({"link_key": link_key})
                substitutions = create_effsat_substitutions(substitution_values)
                substitutions["model_type"] = "EFFSATS"
                substitutions["effsat_name"] = name

                formatted_effsat_name = substitution_values["file_name"].lower()
                write_model_files(
                    substitutions,
                    link_template,
                    formatted_effsat_name,
                )


def create_effsat_model_files(substitutions, link_template, file_name):
    link_model = link_template.substitute(substitutions)
    with open(f"./models/raw_vault/sats/eff_sat_{file_name}.sql", "w") as sql_export:
        sql_export.write(link_model)


def create_effsat_substitutions(substitution_values):
    source = substitution_values["source"]
    link_keys = substitution_values["hubs"]
    short_name = substitution_values["link_key"]
    table_name = f'"stg_{source.lower()}"'
    hash_key = (short_name + "_HK").upper()

    src_dfk = f"{link_keys[0]}_HK"
    dependent_keys = link_keys[1:]

    src_fk = f",\n{chr(32)*19}".join(
        [f'"{combination}_HK"' for combination in dependent_keys]
    )
    src_start_date = "START_DATE"
    src_end_date = "END_DATE"
    src_eff = "EFFECTIVE_FROM"
    load_datetime = "LOAD_DATETIME"
    record_source = "RECORD_SOURCE"
    substitutions = {
        "source_model": table_name,
        "src_pk": hash_key,
        "src_dfk": src_dfk,
        "src_fk": src_fk,
        "src_start_date": src_start_date,
        "src_start_date": src_end_date,
        "src_eff": src_eff,
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
    link_source_map = {
        file_path: f'{"_".join(list(get_map_of_source_and_hubs(metadata).values())[0])}_{Metadata(metadata).get_unit_of_work()}'
        for file_path, metadata in file_map.items()
        if len(list(get_map_of_source_and_hubs(metadata).values())[0]) > 1
    }
    return link_source_map


def get_map_of_source_and_hubs(metadata):
    read_metadata = Metadata(metadata)
    hubs = read_metadata.get_hubs_from_business_topics()
    return {read_metadata.get_versioned_source_name(): hubs}


if __name__ == "__main__":
    export_all_effsat_files()
