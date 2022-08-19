from generate_raw_vault.app.find_metadata_files import (
    load_metadata_file,
    find_json_metadata,
)
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
    versioned_source_name = metadata.get_versioned_source_name().upper()
    transactional_payloads = metadata.get_transactional_payloads()
    hub_names_list = metadata.get_hubs_from_business_topics()
    primary_key_datatype_association = {}
    transactional_payload_columns_and_types_str = ""

    for hub_name in hub_names_list:
        primarykey_datatype_map = metadata.get_primarykey_datatype_map(
            metadata.get_business_keys().get(hub_name)
        )
        for primarykey, datatype in primarykey_datatype_map.items():
            primary_key_datatype_association[primarykey] = datatype
    keys_and_types_str = format_column_and_dtype(primary_key_datatype_association)
    payload_columns = metadata.get_source_attributes()
    payload_columns_and_types = {
        list(column_and_type.keys())[0]: list(column_and_type.values())[0].get("type")
        for column_and_type in payload_columns
    }
    payload_columns_and_types_str = format_column_and_dtype(payload_columns_and_types)
    if transactional_payloads:
        transactional_payload_datatype_map = (
            metadata.get_transactional_payload_datatype_map(transactional_payloads)
        )
        transactional_payload_columns_and_types_str = format_column_and_dtype(
            transactional_payload_datatype_map
        )
        ddl_statement = create_ddl_with_transaction_payload_statement(
            keys_and_types_str,
            payload_columns_and_types_str,
            transactional_payload_columns_and_types_str,
            target_database,
            target_schema,
            versioned_source_name,
        )
    else:
        ddl_statement = create_ddl_without_transaction_payload_statement(
            keys_and_types_str,
            payload_columns_and_types_str,
            target_database,
            target_schema,
            versioned_source_name,
        )
    return ddl_statement


def create_ddl_with_transaction_payload_statement(
    keys_and_types_str,
    column_and_types_str,
    transactional_payload_columns_and_types_str,
    target_database,
    target_schema,
    source_name,
):
    ddl = f"""CREATE TABLE "{target_database}"."{target_schema}"."{source_name}" (
    {keys_and_types_str},
    {column_and_types_str},
    {transactional_payload_columns_and_types_str},
    "RECORD_SOURCE" STRING,
    "LOAD_DATETIME" TIMESTAMP_TZ
    );\n"""
    return ddl


def create_ddl_without_transaction_payload_statement(
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
    );\n"""
    return ddl


def format_column_and_dtype(columns_and_types):
    list_of_column_types = [
        f'"{column}" {column_type}' for column, column_type in columns_and_types.items()
    ]
    deduped_column_types = sorted(set(list_of_column_types))
    column_and_types_str = f",\n{4*chr(32)}".join(deduped_column_types)
    return column_and_types_str


if __name__ == "__main__":
    metadata_file_dirs = find_json_metadata(metadata_directory="source_metadata")
    export_all_ddl_statments(metadata_file_dirs)
