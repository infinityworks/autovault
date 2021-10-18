from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template


def export_all_hub_files():
    metadata_file_dirs = find_json_metadata("source_metadata")
    for metadata_file_path in metadata_file_dirs:
        create_hub_file(metadata_file_path)


def create_hub_file(metadata_file_path):
    template = load_template_file("generate_raw_vault/app/templates/hub_model.sql")
    hub_template = Template(template)

    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)

    hubs = metadata.get_hubs_from_business_topics()

    for hub in hubs:
        substitutions = create_hub_subsitutions(metadata, hub_name=hub)
        hub_model = hub_template.substitute(substitutions)

        file_name = metadata.get_versioned_source_name().lower()
        with open(f"./models/raw_vault/hubs/{hub.lower()}.sql", "w") as sql_export:
            sql_export.write(hub_model)


def create_hub_subsitutions(metadata, hub_name):
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    source_name = f"{database_name}_{schema_name}"
    table_name = metadata.get_versioned_source_name().lower()

    primary_key = metadata.get_hub_business_key(hub_name)
    hash_key = f'src_pk = "{hub_name}_HK"'
    hub_natural_key = f'src_nk = "{primary_key}"'
    load_datetime = f'src_ldts = "LOAD_DATETIME"'
    record_source = f'src_source = "RECORD_SOURCE"'

    substitutions = {
        "source_model": f'source_model = "stg_{table_name}"',
        "src_pk": hash_key,
        "src_nk": hub_natural_key,
        "src_ldts": load_datetime,
        "src_source": record_source,
    }

    return substitutions


if __name__ == "__main__":
    export_all_hub_files()
