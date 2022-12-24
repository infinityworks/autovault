from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.metadata_handler import Metadata
from generate_raw_vault.app.model_creation import write_model_files

from string import Template

SATELLITE_TEMPLATE = "generate_raw_vault/app/templates/sat_model.sql"


def export_all_sat_files(metadata_file_dirs):
    for metadata_file_path in metadata_file_dirs:
        create_sat_file(metadata_file_path)


def create_sat_file(metadata_file_path):
    template = load_template_file(SATELLITE_TEMPLATE)
    sat_template = Template(template)

    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)

    hubs = metadata.get_hubs_from_business_topics()

    source_name = metadata.get_versioned_source_name().lower()
    source_system = metadata.get_source_system().lower()
    source_version = metadata.get_source_version().lower()
    for hub_name in hubs:
        satellites_details_in_hub = metadata.get_sat_from_hub(hub_name)
        if satellites_details_in_hub:
            satellites = {
                business_definition: payload
                for business_definition, payload in satellites_details_in_hub.items()
                if payload is not None
            }
            for satellite in satellites:
                sat_name = f"{source_system}_{satellite.lower()}_v{source_version}"
                substitutions = create_sat_substitutions(
                    source_name, satellite, satellites, hub_name, sat_name
                )
                substitutions["model_type"] = "SATS"
                write_model_files(
                    substitutions,
                    sat_template,
                    filename=sat_name,
                )


def format_columns(column_list):
    formatted_list = [f'"{column}"' for column in column_list]
    return f"\n{chr(32)*2}- ".join(formatted_list)


def create_sat_substitutions(source_name, satellite, satellites, hub_name, sat_name):
    hash_primary_key = f'src_pk: "{hub_name}_HK"'
    hashdiff_column = f'source_column: "{satellite}_HASHDIFF"'

    sorted_source_attributes = sorted(list(satellites[satellite].keys()))
    columns = format_columns(sorted_source_attributes)
    substitutions = {
        "sat_name": sat_name,
        "source_model": f'source_model: "stg_{source_name}"',
        "src_pk": hash_primary_key,
        "src_hashdiff_column": hashdiff_column,
        "payload": f"- {columns}",
    }
    return substitutions


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    export_all_sat_files(metadata_file_dirs)
