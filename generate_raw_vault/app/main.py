import json
import itertools
from generate_raw_vault.app.find_metadata_files import find_json_metadata
from generate_raw_vault.app.export_ddl_statement import ddl_exporter
from generate_raw_vault.app.create_model_schema import export_model_schema


def main():
    metadata_file_dirs = find_json_metadata(parent_dir="source_metadata")
    for metadata_file_path in metadata_file_dirs:
        ddl_exporter(metadata_file_path)
    export_model_schema(metadata_file_dirs)
    # create_hubs()
    # create_stages()
    # create_sats()
    # create_links()


if __name__ == "__main__":
    main()
