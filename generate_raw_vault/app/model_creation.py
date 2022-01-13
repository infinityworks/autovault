def create_model_files(substitutions, model_template, model_type, filename):
    model = model_template.substitute(substitutions)
    with open(f"./models/raw_vault/{model_type}/{filename}.sql", "w") as dbt_sql_export:
        dbt_sql_export.write(model)


def create_substitution_values_template():
    return {
        "hubs": "",
        "filename": "",
        "link_name": "",
        "source_list": [],
        "record_load_datetime": "LOAD_DATETIME",
        "record_source": "RECORD_SOURCE",
    }
