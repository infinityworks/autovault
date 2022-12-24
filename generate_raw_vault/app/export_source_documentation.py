from pathlib import Path
from generate_raw_vault.app.find_metadata_files import (
    find_json_metadata,
    load_metadata_file,
    load_template,
)
from generate_raw_vault.app.metadata_handler import Metadata
from generate_raw_vault.app.model_creation import (
    write_documentation_files,
)


def export_all_model_docs_md_files(metadata_file_dirs):
    DOCS_TEMPLATE = "generate_raw_vault/app/templates/documentation.md"
    template = load_template(DOCS_TEMPLATE)
    all_metadata = {
        str(metadata_file_path): Metadata(load_metadata_file(metadata_file_path))
        for metadata_file_path in metadata_file_dirs
    }

    subsitutions = {
        source_file: create_substitution_values(metadata)
        for source_file, metadata in all_metadata.items()
    }
    for substitution in subsitutions.values():
        filename = substitution.get("versioned_source_name").lower()
        write_documentation_files(substitution, template, filename)


def create_substitution_values(metadata):
    substitutions = {
        "versioned_source_name_desc": metadata.get_versioned_source_name_desc(),
        "versioned_source_name": metadata.get_versioned_source_name(),
        "table_description": metadata.get_table_description(),
        "unit_of_work": metadata.get_unit_of_work(),
        "source_name": metadata.get_source_name(),
        "version": metadata.get_source_version(),
        "freshness": metadata.get_freshness(),
        "format": metadata.get_file_format(),
        "filetype": metadata.get_filetype(),
        "source_location": metadata.get_source_location(),
        "warehouse_location": metadata.get_warehouse_location(),
        "access_roles": metadata.get_access_roles(),
        "access_requests": metadata.get_access_requests(),
        "maintained_by": metadata.get_maintained_by(),
        "quality": metadata.get_data_quality(),
    }
    return substitutions


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    export_all_model_docs_md_files(metadata_file_dirs)
