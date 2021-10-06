import json
import itertools

def load_metadata_file(metadata_path:str):
    with open(metadata_path) as metadata_file:
        metadata = json.load(metadata_file)
    return metadata

def get_business_topics(metadata):
    business_topics = metadata.get("business_topics")
    return business_topics

def get_hubs_from_business_topics(business_topics):
    list_business_topics = list(business_topics.keys())
    return list_business_topics

def get_sats_from_hub(business_topics, hub):
    topics = business_topics.get(hub)
    sats = {hub : [topic.get("business_definition") for topic in topics]}
    return sats


def export_source_ddl(ddl, source_name):
    formatted_source_name = source_name.lower()
    with open(f"./source_tables/DDL/{formatted_source_name}.sql", "w") as sql_export:
        sql_export.write(ddl)

def create_source_table_ddl(metadata, database, schema):
    source_name = metadata.get("source_name")
    business_keys = get_source_business_keys(metadata)
    payload = [f'''{list(business_key.keys())[0]} {list(business_key.values())[0]}''' for business_key in business_keys]
    payload_columns = f",\n{4*chr(32)}".join(payload)
    ddl = f'''CREATE TABLE IF NOT EXISTS {database}.{schema}.{source_name} (
    {payload_columns},
    RECORD_SOURCE STRING, 
    LOAD_DATETIME TIMESTAMP_TZ
    )
    '''
    return ddl


def get_source_business_keys(metadata):
    topics = [topic for topic in metadata.get("business_topics").values()]
    source_keys = format_business_key_list(topics)
    return source_keys

def format_business_key_list(source_topics):
    source_keys = [hub_info.get("business_keys") for hub_info in source_topics]
    return source_keys

# get_source_payload columns, similar to above
# may be useful -> list(itertools.chain(*source_keys))

if __name__ == '__main__':
    metadata = load_metadata_file('./source_metadata/customers.json')
    business_topics = get_business_topics(metadata)
    
    hubs = get_hubs_from_business_topics(business_topics)

    source_business_keys = get_source_business_keys(metadata)
    ddl  = create_source_table_ddl(metadata, database="AUTOVAULT", schema="PUBLIC")
    print(ddl)
    export_source_ddl(ddl, source_name= "CUSTOMERS")
    