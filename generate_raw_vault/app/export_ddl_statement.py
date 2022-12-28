from generate_raw_vault.app.find_metadata_files import (
    load_metadata_file,
    find_json_metadata,
    load_template,
)
from generate_raw_vault.app.model_creation import (
    write_ddl_file,
)
from generate_raw_vault.app.metadata_handler import Metadata
from pathlib import Path

DDL_TEMPLATE = "generate_raw_vault/app/templates/ddl.sql"


def export_all_ddl_statments(metadata_file_dirs):
    for metadata_file_path in metadata_file_dirs:
        ddl_exporter(metadata_file_path)


def ddl_exporter(metadata_file_path):
    json_metadata = load_metadata_file(metadata_file_path)
    metadata = Metadata(json_metadata)
    template = load_template(DDL_TEMPLATE)
    ddl_substitutions = create_source_table_ddl(metadata)
    formatted_source_name = metadata.get_versioned_source_name().lower()
    write_ddl_file(ddl_substitutions, template, formatted_source_name)


def create_source_table_ddl(metadata):
    target_database = metadata.get_target_database()
    target_schema = metadata.get_target_schema()
    versioned_source_name = metadata.get_versioned_source_name().upper()
    transactional_payloads = metadata.get_transactional_payloads()
    hub_names_list = metadata.get_hubs_from_business_topics()
    access_roles = metadata.metadata.get("access_roles")
    primary_key_datatype_association = {}
    transactional_payload_columns_and_types_str = ""

    for hub_name in hub_names_list:
        primarykey_datatype_map = metadata.get_key_datatype_map(
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
        payload_columns_and_types_str += (
            f",\n{4*chr(32)}{transactional_payload_columns_and_types_str}"
        )

    substitutions = {
        "target_database": target_database,
        "target_schema": target_schema,
        "versioned_source_name": versioned_source_name,
        "keys_and_types_str": keys_and_types_str,
        "payload_columns_and_types_str": payload_columns_and_types_str,
    }

    if access_roles:
        grants_list = [
            f'GRANT SELECT ON "{target_database}"."{target_schema}"."{versioned_source_name}" TO ROLE "{role}";\n'
            for role in access_roles
        ]
        access_grants = "".join(grants_list)
        substitutions["access_grants"] = access_grants
    else:
        substitutions["access_grants"] = ""
    return substitutions


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
