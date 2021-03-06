from generate_raw_vault.app.find_metadata_files import find_json_metadata
from generate_raw_vault.app.export_model_schema_yml import export_model_schema
from generate_raw_vault.app.export_ddl_statement import export_all_ddl_statments
from generate_raw_vault.app.export_staging_vault_models import export_all_staging_files
from generate_raw_vault.app.export_hub_vault_models import export_all_hub_files
from generate_raw_vault.app.export_satellite_vault_models import export_all_sat_files
from generate_raw_vault.app.export_link_vault_models import export_all_link_files
from generate_raw_vault.app.export_effsat_vault_models import export_all_effsat_files
from create_model_directories import create_directory_and_gitkeep


def main():
    model_directories = [
        "./source_metadata",
        "./source_tables/ddl",
        "./models/raw_vault/hubs",
        "./models/raw_vault/links",
        "./models/raw_vault/sats",
        "./models/raw_vault/stages",
    ]
    for directory in model_directories:
        create_directory_and_gitkeep(directory)
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")

    export_all_ddl_statments(metadata_file_dirs)
    export_all_hub_files(metadata_file_dirs)
    export_all_link_files(metadata_file_dirs)
    export_model_schema(metadata_file_dirs)
    export_all_sat_files(metadata_file_dirs)
    export_all_effsat_files()
    export_all_staging_files(metadata_file_dirs)


if __name__ == "__main__":
    main()
