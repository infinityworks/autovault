from generate_raw_vault.app.find_metadata_files import (
    find_json_metadata,
    load_metadata_file,
    load_template,
)
from generate_raw_vault.app.metadata_handler import Metadata
from string import Template
from pathlib import Path

SOURCE_TEMPLATE = "generate_raw_vault/app/templates/data_source.sql"
MODEL_SCHEMA_TEMPLATE = "generate_raw_vault/app/templates/model_schema.sql"
SCHEMA_YML_PATH = "./models/schema.yml"


def export_model_schema(metadata_file_dirs: list):
    sources_files = {
        str(file): get_individual_source(file) for file in metadata_file_dirs
    }

    aggregated_sources = {
        source.get("source_name"): create_sources_map(source)
        for source in sources_files.values()
    }

    for original_source in sources_files.values():
        aggregated_sources[original_source.get("source_name")].get("tables").append(
            original_source.get("table")
        )

    for source_name in aggregated_sources.keys():
        format_source_table_list(aggregated_sources[source_name])

    source_template = load_template(SOURCE_TEMPLATE)
    source_string_map = generate_source_substitutions(
        source_template=source_template, aggregated_sources=aggregated_sources
    )
    model_template = load_template(MODEL_SCHEMA_TEMPLATE)
    schema_yml = model_template.substitute(source_string_map)

    with open(Path(SCHEMA_YML_PATH), "w") as schema_yml_export:
        schema_yml_export.write(schema_yml)
    return schema_yml


def get_individual_source(file: Path) -> dict:
    metadata_file = load_metadata_file(file)
    metadata = Metadata(metadata_file)
    return create_schema_subsitutions(metadata)


def create_schema_subsitutions(metadata) -> dict:
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    source_name = f"{database_name}_{schema_name}"
    hub_names_list = metadata.get_hubs_from_business_topics()
    primary_keys = []
    for hub_name in hub_names_list:
        primarykey_datatype_map = metadata.get_primarykey_datatype_map(
            metadata.get_business_keys().get(hub_name)
        )
        for primarykey in primarykey_datatype_map.keys():
            primary_keys.append(f"{10*chr(32)}- name: {primarykey}")
            primarykey_description_map = metadata.get_primarykey_description_map(
                metadata.get_business_keys().get(hub_name)
            )
            primarykey_test_map = metadata.get_primary_key_tests_map(
                metadata.get_business_keys().get(hub_name)
            )
            for description in primarykey_description_map.values():
                primary_keys.append(
                    f'{12*chr(32)}description: "{description}"\n{12*chr(32)}tests:'
                )
            for test, test_type in primarykey_test_map.items():
                primary_keys.append(f"{12*chr(32)}{chr(32)} - {test}")
    keys_str = "\n".join(primary_keys)
    table_name = f"- name: {metadata.get_versioned_source_name()}\n{8*chr(32)}columns:\n{keys_str}"
    substitutions = {
        "source_name": source_name,
        "database": database_name,
        "schema": schema_name,
        "table": table_name,
    }
    return substitutions


def create_sources_map(source: dict) -> dict:
    source = {
        "source_name": source.get("source_name"),
        "tables": [],
        "database": source.get("database"),
        "schema": source.get("schema"),
        "business_keys": source.get("business_keys"),
    }
    return source


def format_source_table_list(source: dict) -> dict:
    sorted_table_list = sorted(source["tables"])
    yml_padder = f"\n{6*chr(32)}"
    source["tables"] = yml_padder.join(sorted_table_list)
    return source


def generate_source_substitutions(
    source_template: Template, aggregated_sources: dict
) -> str:
    source_name_list = sorted(
        [source_name for source_name in aggregated_sources.keys()]
    )
    source_string_list = [
        generate_source_str(source_template, aggregated_sources[name])
        for name in source_name_list
    ]
    source_string_map = {"sources": "  ".join(source_string_list)}
    return source_string_map


def generate_source_str(source_template: Template, substitutions: dict) -> dict:
    schema_yml = source_template.substitute(substitutions)
    return schema_yml


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    subs = export_model_schema(metadata_file_dirs)
