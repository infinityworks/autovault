from generate_raw_vault.app.find_metadata_files import load_metadata_file
from generate_raw_vault.app.metadata_handler import Metadata
from pathlib import Path


def export_all_ddl_statments(metadata_file_dirs):
    for metadata_file_path in metadata_file_dirs:
        ddl_exporter(metadata_file_path)


def ddl_exporter(metadata_file_path):
    json_metadata = load_metadata_file(metadata_file_path)
    metadata = Metadata(json_metadata)
    ddl = create_source_table_ddl(metadata)
    formatted_source_name = metadata.get_versioned_source_name().lower()
    with open(
        Path(f"./source_tables/ddl/{formatted_source_name}.sql"), "w"
    ) as sql_export:
        sql_export.write(ddl)


def create_source_table_ddl(metadata):
    target_database = metadata.get_target_database()
    target_schema = metadata.get_target_schema()
    versioned_source_name = metadata.get_versioned_source_name()
    business_topics = metadata.get_source_business_topics()
    business_keys = metadata.get_business_keys().values()
    primary_keys = [key.get("natural_keys") for key in business_keys]
    keys_and_types_str = format_column_and_dtype(primary_keys)
    payload_columns = metadata.get_source_attributes()
    payload_columns_and_types_str = format_column_and_dtype(payload_columns)
    ddl_statement = create_ddl_statement(
        keys_and_types_str,
        payload_columns_and_types_str,
        target_database,
        target_schema,
        versioned_source_name,
    )
    return ddl_statement


def create_ddl_statement(
    keys_and_types_str,
    column_and_types_str,
    target_database,
    target_schema,
    source_name,
):
    ddl = f"""CREATE TABLE "{target_database}"."{target_schema}"."{source_name}" (
    {keys_and_types_str},
    {column_and_types_str},
    "RECORD_SOURCE" STRING,
    "LOAD_DATETIME" TIMESTAMP_TZ
    );
    """
    return ddl


def format_column_and_dtype(columns_and_types):
    list_of_column_types = [
        f'"{list(column_and_type.keys())[0]}" {list(column_and_type.values())[0]}'
        for column_and_type in columns_and_types
    ]
    deduped_column_types = sorted(set(list_of_column_types))
    column_and_types_str = f",\n{4*chr(32)}".join(deduped_column_types)
    return column_and_types_str


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    export_all_ddl_statments(metadata_file_dirs)
