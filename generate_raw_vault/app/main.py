from generate_raw_vault.app.find_metadata_files import find_json_metadata
from generate_raw_vault.app.export_model_schema_yml import export_model_schema
from generate_raw_vault.app.export_ddl_statement import ddl_exporter
from generate_raw_vault.app.export_staging_vault_models import export_all_staging_files
from generate_raw_vault.app.export_hub_vault_models import export_all_hub_files
from generate_raw_vault.app.export_satellite_vault_models import export_all_sat_files


def main():
    metadata_file_dirs = find_json_metadata(parent_dir="source_metadata")
    for metadata_file_path in metadata_file_dirs:
        ddl_exporter(metadata_file_path)
    export_model_schema(metadata_file_dirs)
    export_all_staging_files()
    export_all_hub_files()
    export_all_staging_files()
    export_all_sat_files()
    # create_links()


if __name__ == "__main__":
    main()
