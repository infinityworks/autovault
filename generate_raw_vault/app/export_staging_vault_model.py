from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template

template = load_template_file("generate_raw_vault/app/templates/staging_model.sql")
staging_template = Template(template)

metadata_file = load_metadata_file("source_metadata/customers_v1.json")
metadata = Metadata(metadata_file)


def format_derived_columns(column_list):
    return "\n  ".join(column_list)


def format_columns(column_list):
    formatted_list = [f'"{column}"' for column in column_list]
    return f"\n{chr(32)*6}- ".join(formatted_list)


def create_staging_subsitutions(metadata, hub_name):
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    source_name = f"{database_name}_{schema_name}"
    table_name = metadata.get_versioned_source_name()

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


substitutions = create_staging_subsitutions(metadata, hub_name="CUSTOMER")
staging_model = staging_template.substitute(substitutions)


file_name = metadata.get_versioned_source_name().lower()
with open(f"./models/stage/stg_{file_name}.sql", "w") as sql_export:
    sql_export.write(staging_model)
