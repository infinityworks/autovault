from generate_raw_vault.app.find_metadata_files import (
    load_template_file,
    load_metadata_file,
    find_json_metadata,
)
from generate_raw_vault.app.load_metadata import Metadata
from string import Template
import json
import itertools
import glob
from pathlib import Path


def find_links(parent_dir):
    link_files = [
        Path(file).name
        for file in glob.iglob(f"models/raw_Vault/links/*.sql", recursive=True)
    ]
    print(link_files)
    print(list(map(lambda h: h.replace(".sql", ""), link_files)))
    # print(glob.iglob(f"./{parent_dir}/links/*.sql"))
    # return metadata_files


def export_all_link_files():
    metadata_file_dirs = find_json_metadata("source_metadata")
    for metadata_file_path in metadata_file_dirs:
        print(metadata_file_path)
        create_link_file(metadata_file_path)


# def create_link_file(metadata_file_path):
#     template = load_template_file("generate_raw_vault/app/templates/link_model.sql")
#     link_template = Template(template)

#     metadata_file = load_metadata_file(metadata_file_path)
#     metadata = Metadata(metadata_file)

#     hubs = metadata.get_hubs_from_business_topics()
#     for hub in hubs:
#         substitutions = create_link_subsitutions(metadata, hub_name=hub)
#         print(hub)
#         # print(json.dumps(substitutions, indent=4), "\n")
#         link_model = link_template.substitute(substitutions)

#         file_name = metadata.get_versioned_source_name().lower()
#         with open(f"./models/raw_vault/links/{file_name}.sql", "w") as sql_export:
#             sql_export.write(link_model)


def create_link_file(metadata_file_path):
    template = load_template_file("generate_raw_vault/app/templates/link_model.sql")
    link_template = Template(template)

    metadata_file = load_metadata_file(metadata_file_path)
    metadata = Metadata(metadata_file)

    hubs = metadata.get_hubs_from_business_topics()
    print(sorted(hubs))
    #     for v in itertools.combinations(['A', 'B', 'C'], 2):
    # ...   print(v)
    for v in itertools.combinations(sorted(hubs), 2):
        print(v)
        file_name = f'{"_".join(sorted(v))}'
        print(file_name.lower())
        # for hub in hubs:
        substitutions = create_link_subsitutions(metadata, v)

        # print(json.dumps(substitutions, indent=4), "\n")
        link_model = link_template.substitute(substitutions)
        file_name = f'{"_".join(sorted(v))}'.lower()
        with open(f"./models/raw_vault/links/{file_name}.sql", "w") as sql_export:
            sql_export.write(link_model)


def format_derived_columns(column_list):
    return "\n  ".join(column_list)


def format_columns(column_list):
    if "null" in column_list:
        column_list.remove("null")
    formatted_list = [f'"{column}"' for column in column_list]
    return f"\n{chr(32)*6}- ".join(formatted_list)


# def create_link_subsitutions(metadata, hub_name):
#     database_name = metadata.get_target_database()
#     schema_name = metadata.get_target_schema()
#     source_name = f"{database_name}_{schema_name}"
#     table_name = metadata.get_versioned_source_name()

#     # derive hubs and their keys, output list of keys
#     # derived_columns = [
#     #     'EFFECTIVE_FROM: "LOAD_DATETIME"',
#     #     'START_DATE: "LOAD_DATETIME"',
#     #     '''END_DATE: "TO_DATE('9999-12-31')"''',
#     # ]
#     # formatted_derived_columns = format_derived_columns(derived_columns)

#     # primary_key = metadata.get_hub_business_key(hub_name)
#     # hash_key = f'{hub_name}_HK: "{primary_key}"'
#     hubs = metadata.get_hubs_from_business_topics()
#     hash_key = f'{"_".join(sorted(hubs))}_HK'
#     # print(hubs)
#     # print(hash_key)
#     src_fk = list(map(lambda h: h + "_HK", hubs))
#     # print(src_fk)
#     load_datetime = "LOAD_DATETIME"
#     record_source = "RECORD_SOURCE"

#     # hashdiff = f"{hub_name}_HASHDIFF"

#     # source_attributes = [
#     #     list(col.keys())[0] for col in metadata.get_source_attributes()
#     # ]

#     # columns = format_columns(source_attributes)

#     substitutions = {
#         "source_model": table_name.lower(),
#         "src_pk": hash_key,
#         "src_fk": src_fk,
#         "src_ldts": load_datetime,
#         "src_source": record_source,
#     }
#     # print(substitutions)
#     return substitutions


def create_link_subsitutions(metadata, hubs):
    # database_name = metadata.get_target_database()
    # schema_name = metadata.get_target_schema()
    # source_name = f"{database_name}_{schema_name}"
    table_name = metadata.get_versioned_source_name()

    # derive hubs and their keys, output list of keys
    # derived_columns = [
    #     'EFFECTIVE_FROM: "LOAD_DATETIME"',
    #     'START_DATE: "LOAD_DATETIME"',
    #     '''END_DATE: "TO_DATE('9999-12-31')"''',
    # ]
    # formatted_derived_columns = format_derived_columns(derived_columns)

    # primary_key = metadata.get_hub_business_key(hub_name)
    # hash_key = f'{hub_name}_HK: "{primary_key}"'

    hash_key = f'{"_".join(sorted(hubs))}_HK'
    # print(hubs)
    # print(hash_key)
    src_fk = json.dumps(list(map(lambda h: h + "_HK", sorted(hubs))))
    # print(src_fk)
    load_datetime = "LOAD_DATETIME"
    record_source = "RECORD_SOURCE"

    # hashdiff = f"{hub_name}_HASHDIFF"

    # source_attributes = [
    #     list(col.keys())[0] for col in metadata.get_source_attributes()
    # ]

    # columns = format_columns(source_attributes)

    substitutions = {
        "source_model": table_name.lower(),
        "src_pk": hash_key,
        "src_fk": src_fk,
        "src_ldts": load_datetime,
        "src_source": record_source,
    }
    print(substitutions.get("source_model"))
    return substitutions


if __name__ == "__main__":
    export_all_link_files()
    # find_links("generate_raw_vault")
