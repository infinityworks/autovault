from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template
import json

STAGING_TEMPLATE = "generate_raw_vault/app/templates/staging_model.txt"


def export_all_staging_files():
    metadata_file_dirs = find_json_metadata("source_metadata")
    for metadata_file_path in metadata_file_dirs:
        create_staging_file(metadata_file_path)


def create_staging_file(metadata_file_path):
    template = load_template_file(STAGING_TEMPLATE)
    staging_template = Template(template)

    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)

    hubs = metadata.get_hubs_from_business_topics()

    for hub in hubs:
        substitutions = create_staging_subsitutions(metadata, hub_name=hub)
        # print(hub)
        print(json.dumps(substitutions, indent=4), "\n")
        staging_model = staging_template.substitute(substitutions)

        file_name = metadata.get_versioned_source_name().lower()
        with open(f"./models/raw_vault/stages/stg_{file_name}.sql", "w") as sql_export:
            sql_export.write(staging_model)


def format_derived_columns(column_list):
    return "\n  ".join(column_list)


def format_columns(column_list):
    if "null" in column_list:
        column_list.remove("null")
    formatted_list = [f'"{column}"' for column in column_list]
    return f"\n{chr(32)*6}- ".join(formatted_list)


def create_staging_subsitutions(metadata, hub_name):
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    source_name = f"{database_name}_{schema_name}"
    table_name = metadata.get_versioned_source_name()

    # derive hubs and their keys, output list of keys
    derived_columns = [
        'EFFECTIVE_FROM: "LOAD_DATETIME"',
        'START_DATE: "LOAD_DATETIME"',
        '''END_DATE: "TO_DATE('9999-12-31')"''',
    ]
    formatted_derived_columns = format_derived_columns(derived_columns)

    primary_key = metadata.get_hub_business_key(hub_name)
    hash_key = f'{hub_name}_HK: "{primary_key}"'

    hashdiff = f"{hub_name}_HASHDIFF"

    source_attributes = [
        list(col.keys())[0] for col in metadata.get_source_attributes()
    ]

    columns = format_columns(source_attributes)

    substitutions = {
        "source": f'{source_name}: "{table_name}"',
        "derived_columns": formatted_derived_columns,
        "hashed_primary_key": hash_key,
        "hashdiff": hashdiff,
        "columns": f"- {columns}",
    }

    return substitutions


if __name__ == "__main__":
    export_all_staging_files()
