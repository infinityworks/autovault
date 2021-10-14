from generate_raw_vault.app.find_metadata_files import find_json_metadata
from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template
from pathlib import Path
import json


def export_model_schema(metadata_file_path):
    metadata_files = [
        "./source_metadata/customers_v1.json",
        "./source_metadata/products_v1.json",
        "./source_metadata/transactions_v1.json",
    ]
    individual_sources = {}
    for file in metadata_files:
        metadata_file = load_metadata_file(file)
        metadata = Metadata(metadata_file)

        substitutions = create_schema_subsitutions(metadata)
        individual_sources.update({get_name(metadata): substitutions})

    sources = {
        source.get("name"): {
            "name": source.get("name"),
            "tables": [],
            "database": source.get("database"),
            "schema": source.get("schema"),
        }
        for source in individual_sources.values()
    }

    for source in individual_sources.values():
        sources[source.get("name")]["tables"].append(f"- name: {source.get('tables')}")

    sources["AUTOVAULT_PUBLIC"]["tables"] = format_table_list(
        sources["AUTOVAULT_PUBLIC"]["tables"]
    )

    print(sources)
    template_file = load_template_file(
        "generate_raw_vault/app/templates/model_schema.yml"
    )
    model_template = Template(template_file)
    substitutions = sources["AUTOVAULT_PUBLIC"]

    schema_yml = model_template.substitute(substitutions)

    with open(Path(f"./models/schema.yml"), "w") as sql_export:
        sql_export.write(schema_yml)


def get_name(metadata):
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    table_name = metadata.get_versioned_source_name()
    name = "_".join([database_name, schema_name, table_name])
    return name


def format_table_list(table_list):
    return f"\n{chr(32)*6}".join(table_list)


def create_schema_subsitutions(metadata):
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    source_name = f"{database_name}_{schema_name}"
    table_name = metadata.get_versioned_source_name()

    substitutions = {
        "name": source_name,
        "database": database_name,
        "schema": schema_name,
        "tables": table_name,
    }
    return substitutions


if __name__ == "__main__":
    export_model_schema(metadata_file_path="./source_metadata/customers_v1.json")
