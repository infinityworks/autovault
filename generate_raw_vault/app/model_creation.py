from typing import Set, Any
import itertools


def write_model_files(substitutions, model_template, filename):
    model = model_template.substitute(substitutions)
    model_type = substitutions["model_type"]
    path = f"./models/raw_vault/{model_type}/{model_type[:-1]}_{filename}.sql"
    with open(path.lower(), "w") as dbt_sql_export:
        dbt_sql_export.write(model)


def write_documentation_files(substitutions, docs_template, filename):
    doc = docs_template.substitute(substitutions)
    with open(f"./models/source_descriptions/{filename}.md", "w") as dbt_docs_export:
        dbt_docs_export.write(doc)


def write_ddl_file(substitutions, ddl_template, filename):
    ddl = ddl_template.substitute(substitutions)
    with open(f"./source_tables/ddl/{filename}.sql", "w") as ddl_export:
        ddl_export.write(ddl)


def create_substitution_values_template():
    return {
        "filename": None,
        "hash_key": None,
        "hubs": None,
        "hub_name": None,
        "link_name": None,
        "natural_key": None,
        "record_load_datetime": "LOAD_DATETIME",
        "record_source": "RECORD_SOURCE",
        "source_list": [],
    }


def create_set_from_list_of_lists(list_of_lists) -> Set[str]:
    return set(list(itertools.chain(*list_of_lists)))
