from generate_raw_vault.app.find_metadata_files import (
    find_json_metadata,
    load_template_file,
    load_metadata_file,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template
from pathlib import Path, PosixPath
import json


def export_model_schema_yml_for_all_sources():
    metadata_file_dirs = find_json_metadata("source_metadata")
    export_model_schema(metadata_file_dirs)


def export_model_schema(metadata_file_dirs):
    sources_files = {file: get_individual_source(file) for file in metadata_file_dirs}

    sources = {
        source.get("name"): {
            "name": source.get("name"),
            "tables": [],
            "database": source.get("database"),
            "schema": source.get("schema"),
        }
        for source in sources_files.values()
    }

    for source in sources_files.values():
        sources[source.get("name")]["tables"].append(source.get("table"))

    for key in sources.keys():
        sources[key]["tables"] = format_table_list(sources[key]["tables"])

    source_template_file = load_template_file(
        "generate_raw_vault/app/templates/source_schema.txt"
    )
    source_template = Template(source_template_file)

    keys = sorted([key for key in sources.keys()])
    subs = [generate_source_str(source_template, sources[key]) for key in keys]

    model_template_file = load_template_file(
        "generate_raw_vault/app/templates/model_schema.yml"
    )

    model_template = Template(model_template_file)
    reps = {"sources": "  ".join(subs)}
    schema_yml = model_template.substitute(reps)

    with open(Path(f"./models/schema.yml"), "w") as sql_export:
        sql_export.write(schema_yml)
    return schema_yml


def get_individual_source(file):
    metadata_file = load_metadata_file(file)
    metadata = Metadata(metadata_file)
    individual_source = {
        get_source_name_UID(metadata): create_schema_subsitutions(metadata)
    }
    return create_schema_subsitutions(metadata)


def generate_source_str(source_template, substitutions):
    schema_yml = source_template.substitute(substitutions)
    return schema_yml


def get_source_name_UID(metadata):
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    table_name = metadata.get_versioned_source_name()
    name = "_".join([database_name, schema_name, table_name])
    return name


def format_table_list(table_list):
    return f"\n{chr(32)*6}".join(sorted(table_list))


def create_schema_subsitutions(metadata):
    database_name = metadata.get_target_database()
    schema_name = metadata.get_target_schema()
    source_name = f"{database_name}_{schema_name}"
    table_name = f"- name: {metadata.get_versioned_source_name()}"

    substitutions = {
        "name": source_name,
        "database": database_name,
        "schema": schema_name,
        "table": table_name,
    }
    return substitutions


if __name__ == "__main__":
    subs = export_model_schema_yml_for_all_sources()
