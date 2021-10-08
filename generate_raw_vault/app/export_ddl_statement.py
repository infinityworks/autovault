import json
import itertools
import glob

def export_all_ddl_statments():
    metadata_file_dirs = find_json_metadata()
    for metadata_file_path in metadata_file_dirs:
        ddl_exporter(metadata_file_path)


def ddl_exporter(metadata_file_path):
    metadata = load_metadata_file(metadata_file_path)
    versioned_source_name = format_versioned_source_name(metadata)
    ddl  = create_source_table_ddl(metadata, versioned_source_name, target_database="AUTOVAULT", target_schema="PUBLIC")
    formatted_source_name = versioned_source_name.lower()
    with open(f"./source_tables/DDL/{formatted_source_name}.sql", "w") as sql_export:
        sql_export.write(ddl)


def find_json_metadata():
    metadata_files = [file for file in glob.iglob("./source_metadata/**/*.json", recursive=True)]
    return metadata_files


def create_source_table_ddl(metadata, versioned_source_name, target_database, target_schema):
    business_topics = get_source_business_topics(metadata)
    primary_keys = get_business_key_list(business_topics)
    keys_and_types_str = format_column_and_dtype(primary_keys)
    payload_columns = get_source_payload_list(metadata)
    column_and_types_str = format_column_and_dtype(payload_columns)
    ddl_statement = create_ddl_statement(keys_and_types_str, column_and_types_str, target_database, target_schema, versioned_source_name)
    return ddl_statement

def format_versioned_source_name(metadata):
    source_name = metadata.get("source_name")
    version = "".join(["V",metadata.get("version")])
    versioned_source_name = '_'.join([source_name, version])
    return versioned_source_name


def create_ddl_statement(keys_and_types_str, column_and_types_str, target_database, target_schema, source_name):
    ddl = f'''CREATE TABLE {target_database}.{target_schema}.{source_name} (
    {keys_and_types_str},
    {column_and_types_str},
    RECORD_SOURCE STRING, 
    LOAD_DATETIME TIMESTAMP_TZ
    )
    '''
    return ddl

def format_column_and_dtype(columns_and_types):
    x = [f'''{list(column_and_type.keys())[0]} {list(column_and_type.values())[0]}''' for column_and_type in columns_and_types]
    column_and_types_str = f",\n{4*chr(32)}".join(x)
    return column_and_types_str

def get_source_business_topics(metadata):
    topics = [topic for topic in metadata.get("business_topics").values()]
    return topics


def get_business_key_list(source_topics):
    source_keys = [hub_info.get("business_keys") for hub_info in source_topics]
    return source_keys


def get_source_payload_list(metadata):
    topics = get_source_business_topics(metadata)
    flattened_business_attributes = flatten_business_attributes(topics)
    source_attributes = flatten_source_attributes(flattened_business_attributes)
    return source_attributes


def flatten_source_attributes(flattened_business_attributes):
    source_attributes = [get_attributes(attr) for attr in flattened_business_attributes]
    flatten_source_attributes = list(itertools.chain(*source_attributes))
    return flatten_source_attributes


def flatten_business_attributes(topics):
    business_attributes = [topic.get("business_attributes") for topic in topics]
    flatten_business_attributes = list(itertools.chain(*business_attributes))
    return flatten_business_attributes


def get_attributes(attr):
    source_attributes = [{key : value} for key, value in attr.get("payload").items()]
    return source_attributes
    

def load_metadata_file(metadata_path:str):
    with open(metadata_path) as metadata_file:
        metadata = json.load(metadata_file)
    return metadata


if __name__ == '__main__':
    export_all_ddl_statments()
    
    