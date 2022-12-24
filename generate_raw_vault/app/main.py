from generate_raw_vault.app.find_metadata_files import find_json_metadata
from generate_raw_vault.app.export_source_documentation import (
    export_all_model_docs_md_files,
)
from generate_raw_vault.app.export_model_schema_yml import export_model_schema
from generate_raw_vault.app.export_ddl_statement import export_all_ddl_statments
from generate_raw_vault.app.export_staging_vault_models import export_all_staging_files
from generate_raw_vault.app.export_hub_vault_models import export_all_hub_files
from generate_raw_vault.app.export_satellite_vault_models import export_all_sat_files
from generate_raw_vault.app.export_link_vault_models import export_all_link_files
from generate_raw_vault.app.export_effsat_vault_models import export_all_effsat_files
from create_model_directories import create_directory_and_gitkeep


def main(metadata_file_dirs):
    directories_to_create = [
        "./source_metadata",
        "./source_tables/ddl",
        "./models/raw_vault/hubs",
        "./models/raw_vault/links",
        "./models/raw_vault/trans_links",
        "./models/raw_vault/sats",
        "./models/raw_vault/effsats",
        "./models/raw_vault/stages",
    ]
    for directory in directories_to_create:
        create_directory_and_gitkeep(directory)

    export_all_ddl_statments(metadata_file_dirs)
    export_all_model_docs_md_files(metadata_file_dirs)
    export_model_schema(metadata_file_dirs)
    export_all_staging_files(metadata_file_dirs)
    export_all_hub_files(metadata_file_dirs)
    export_all_sat_files(metadata_file_dirs)
    export_all_effsat_files(metadata_file_dirs)
    export_all_link_files(metadata_file_dirs)


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    # from pathlib import PosixPath; metadata_file_dirs = [PosixPath("/Users/adam.dewberry/Documents/autovault/source_metadata/transactions_v1.json")]
    main(metadata_file_dirs)
