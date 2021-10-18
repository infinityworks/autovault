from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template


def export_all_sat_files():
    metadata_file_dirs = find_json_metadata("source_metadata")
    for metadata_file_path in metadata_file_dirs:
        create_sat_file(metadata_file_path)


def create_sat_file(metadata_file_path):
    template = load_template_file("generate_raw_vault/app/templates/sat_model.txt")
    sat_template = Template(template)

    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)

    hubs = metadata.get_hubs_from_business_topics()

    for hub in hubs:
        substitutions = create_sat_subsitutions(metadata, hub_name=hub)
        sat_model = sat_template.substitute(substitutions)

        file_name = metadata.get_versioned_source_name().lower()
        with open(f"./models/raw_vault/sats/{file_name}.sql", "w") as sql_export:
            sql_export.write(sat_model)


def format_columns(column_list):
    if "null" in column_list:
        column_list.remove("null")
    formatted_list = [f'"{column}"' for column in column_list]
    return f"\n{chr(32)*2}- ".join(formatted_list)


def create_sat_subsitutions(metadata, hub_name):
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    source_name = f"{database_name}_{schema_name}"
    table_name = metadata.get_versioned_source_name().lower()

    primary_key = metadata.get_hub_business_key(hub_name)
    hash_primary_key = f'src_pk: "{hub_name}_HK"'
    hashdiff_column = f'source_column: "{hub_name}_HASHDIFF"'

    source_attributes = [
        list(col.keys())[0] for col in metadata.get_source_attributes()
    ]

    columns = format_columns(source_attributes)

    substitutions = {
        "source_model": f'source_model: "stg_{table_name}"',
        "src_pk": hash_primary_key,
        "src_hashdiff_column": hashdiff_column,
        "payload": f"- {columns}",
    }
    return substitutions


if __name__ == "__main__":
    export_all_sat_files()
