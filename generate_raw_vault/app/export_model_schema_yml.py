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

    for source in sources_files.values():
        aggregated_sources[source.get("source_name")].get("tables").append(
            source.get("table")
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

    hub_attributes = {}
    for hub_name in hub_names_list:
        hub_attributes.update({hub_name: {}})
        hub_business_key_attributes = metadata.get_business_keys().get(hub_name)
        business_keys = hub_business_key_attributes.get("business_keys")
        for key_name, attributes in business_keys.items():
            hub_attributes.get(hub_name).update(
                {f"{key_name}": create_column_descriptions(key_name, attributes)}
            )
        hub_satellites = metadata.get_sat_from_hub(hub_name)
        if hub_satellites:
            for column_name, attributes in list(hub_satellites.values())[0].items():
                hub_attributes.get(hub_name).update(
                    {
                        f"{column_name}": create_column_descriptions(
                            column_name, attributes
                        )
                    }
                )

    joined_key_attributes = {
        hub: "\n".join(list(hub_keys.values()))
        for hub, hub_keys in hub_attributes.items()
    }
    joined_hub_attributes = "\n".join(list(joined_key_attributes.values()))
    table_name = metadata.get_versioned_source_name()
    table_desc = metadata.get_versioned_source_name_desc()
    table_desc_ref = f'{2*chr(123)} doc("{table_desc}") {2*chr(125)}'
    table_description = "\n".join(
        [
            f"- name: {table_name}",
            f"{8*chr(32)}description: '{table_desc_ref}'",
            f"{8*chr(32)}columns:\n{joined_hub_attributes}",
        ]
    )
    substitutions = {
        "source_name": source_name,
        "description": f"{metadata.get_versioned_source_name()}_desc".lower(),
        "database": database_name,
        "schema": schema_name,
        "table": table_description,
    }
    return substitutions


def get_tests(tests):
    column_tests = [
        f"{12*chr(32)}{chr(32)} - {test_type}"
        for test_type, is_active in tests.items()
        if is_active == True
    ]
    return "\n".join(column_tests)


def create_column_descriptions(key_name, attributes):
    descriptions = [f"{10*chr(32)}- name: {key_name}"]
    if attributes.get("description"):
        col_desc = attributes.get("description")
        if attributes.get("driving_key"):
            driving_key = "This is the driving key. "
            col_desc = driving_key + col_desc

        descriptions.append(f'{12*chr(32)}description: "{col_desc}"')
    if attributes.get("description"):
        descriptions.append(f'{12*chr(32)}tests:\n{get_tests(attributes.get("tests"))}')
    column_descriptions = "\n".join(descriptions)
    return column_descriptions


def create_sources_map(source: dict) -> dict:
    source = {
        "source_name": source.get("source_name"),
        "tables": [],
        "description": source.get("description"),
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
