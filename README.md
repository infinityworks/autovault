# Introduction

This project is a framework to automate the creation of a raw vault data model for a Snowflake data warehouse that uses Data Vault 2.0 standards and rules.

The project generates dbt files which build the vault model through defined metadata which describes the source data. Along with generating the dbt files, it also generates SQL DDL statements for creating the landing / staging layer.

The data vault entities produced are:

- Staging enrichment layer (for hashes etc)
- Hubs
- Links
- Satellites

## Dependencies

## Tools

The project relies on the following tools:

- Python 3.8
- dbt 1.0.3
- dbtvault 0.8.1
- pre-commit 2.15.0

Optional:

- snowsql CLI 1.2.21

## Connecting to Snowflake

### Authentication with RSA keys

This project uses rsa keys as secure methods for authentication. To generate a private key edit and run the following cmd

    mkdir -p ~/.ssh/snowsql
    openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out ~/.ssh/snowsql/rsa_key.p8

This will prompt you for a password to encrypt the private key. Each time you connect to Snowflake you will be prompted for the passphrase, alternatively you can export it as an environment variable. If you wish you can include it in your .zshrc file.

    export SNOWSQL_PRIVATE_KEY_PASSPHRASE=<your passphrase>

Create your public key using the private key with the following command:

    openssl rsa -in  ~/.ssh/snowsql/rsa_key.p8 -pubout -out ~/.ssh/snowsql/rsa_key.pub

Attach the public key to the user by executing the below statement in Snowflake UI:

    alter user <firstname.surname@infinityworks.com> set rsa_public_key='<THE_CONTENT_OF_YOUR_RSA_KEY.PUB>';

#### Testing the connection

To test your connection to Snowflake and that dbt can deploy tables and views, you may want to use the snowsql CLI:

Install Snowsql

    brew install snowflake-snowsql

Run snowsql to install the cli; if the cmd is not recognised then add snowsql to your path. To add snowsql to the path on mac, add the following to your .zshrc file.

    export PATH=/Applications/SnowSQL.app/Contents/MacOS:$PATH

[mac only] If .zshrc file does not exist run:

    touch .zshrc

##### Setting up snowsql cli

Populate the the snowsql config file with connection details of your snowflake account and update the options particularly for the log file location.

    [connections.iw]
    accountname = infinityworkspartner
    region = eu-west-1
    role = infra_builder
    username = firstname.surname@infinityworks.com
    warehouse = demo_wh
    private_key_path = /Users/firstname.surname/.ssh/snowsql/rsa_key.p8

    [variables]
    # SnowSQL defines the variables in this section on startup.
    # You can use these variables in SQL statements. For details, see
    # https://docs.snowflake.com/en/user-guide/snowsql-use.html#using-variables

    [options]
    # If set to false auto-completion will not occur interactive mode.
    auto_completion = True
    echo=True
    output_format=fancy_grid
    progress_bar=True
    wrap=False
    log_file = ~/.snowsql/snowsql_rt.log
    # main log file location. The file includes the log from SnowSQL main
    # executable.
    # log_file = ../snowsql_rt.log

    # bootstrap log file location. The file includes the log from SnowSQL bootstrap
    # executable.
    # log_bootstrap_file = ~/.snowsql/log_bootstrap

To test the connection run the snowsql command to your desired profile e.g. `connections.iw`

        snowsql --connection  iw
        !exit

This should validate your connectivity.

## Installing dbt

Create a virtual environment:

    python3 -m venv .venv

Activate the environment

    source .venv/bin/activate

Install dbt

    pip3 install --requirement requirements.txt

### Configure dbt connection to snowflake

If you do not have a dbt profiles.yml, you must create one:

    touch ~/.dbt/profiles.yml

Include the following in the file and change out the relevant account and database details etc:

    default:
        target: "{{ env_var('DBT_PROFILE_TARGET') }}"
        outputs:
            dev:
                type: snowflake
                account: infinityworkspartner.eu-west-1
                user: "{{ env_var('USER') }}@infinityworks.com"
                private_key_path: "{{ env_var('HOME') }}/.ssh/snowsql/rsa_key.p8"
                private_key_passphrase: "{{ env_var('SNOWSQL_PRIVATE_KEY_PASSPHRASE') }}"
                role: INFRA_BUILDER
                database: AUTOVAULT
                warehouse: DEMO_WH
                schema: PUBLIC
                threads: 2
                client_session_keep_alive: False

Export the dbt profile you wish to use, e.g. dev, staging, prod:

    export DBT_PROFILE_TARGET=dev

Test the dbt connection to Snowflake:

    dbt debug

## Installing dbtvault

dbt packages can be [installed via packages.yml](https://hub.getdbt.com/datavault-uk/dbtvault/latest/).

Include the following in your packages.yml file:
packages:

- package: Datavault-UK/dbtvault
    version: 0.7.8

Then run the command:

    dbt deps

## Data sources

Data sources are referenced in schema.yml, this file will be generated from your JSON metadata that descibes your source files and will resemble the following.

    version: 2
    sources:
    - name: AUTOVAULT_PUBLIC (custom name)
        database: AUTOVAULT (your snowflake database)
        schema: PUBLIC (your scheme under)
        tables:
        - name: CUSTOMERS
        - name: PRODUCTS
        - name: TRANSACTIONS
        - name: CUSTOMER_VISITS
        - name: TOTAL_CUST_VISITS

# JSON Metadata

Metadata Template

    {
    “unit_of_work”: “<UNIT_OF_WORK>”,
    “source_name”: “<SOURCE_NAME>”,
    “source_system”: “<SOURCE_SYSTEM>”,
    “version”: “<VERSION>”,
    “destination_database”: “<DESTINATION_DATABASE>”,
    “destination_schema”: “<DESTINATION_SCHEMA>”
    {
    "business_topics": {
        "<BUSINESS_TOPIC_1>": {
        "business_keys": {
                    "<BUSINESS_KEY_1>":"STRING"
                },
        "alias": "<ALIAS_BUSINESS_KEY>",
        "business_attributes": [
            {
            "business_definition": "<BUSINESS_DEFINITION_1>",
            "payload": {
                "COL1": "DECIMAL(38,10)",
                "COL2": "STRING",
                "COL3": "STRING"
            }
            }
        ]
        }
    },
    "<BUSINESS_TOPIC_2>": {
        "business_keys": {
                    "<BUSINESS_KEY_2>>":"STRING"
                },
        "alias": "<ALIAS_BUSINESS_KEY>",
        "business_attributes": [
        {
            "business_definition: "<BUSINESS_DEFINITION_2>",
            "payload": {
            "COL1": "DECIMAL(38,10)",
            "COL2": "STRING"
            }
        }
        ]
    }
    }
    }

## unit_of_work

Unit of work represents the business process or activity that the source table represents. It is used to distinguish between processes/activities with overlapping business topics (hubs).

## source_name

It represents the source name i.e. table name from the source system.

## source_system

It represent the source system the source belongs too.

## version

It is the user defined version of the source system. It is used to identify the changed version of the source system and create a new satellite based on new version of the source.

## destination_database

It the database in snowflake where the raw vault resides.

## destination_schema

It the schema where raw data will land, usually "public".

## business_topic

Concepts such as customer, product, agreement etc. are used to represent ideas, identified as business keys represented across multiple lines of business.

## business_key

The column name/s in the source that stores the business key e.g. customer_id. The business_key should be understood by business and mean something to the business and is exposed to the user. It could be a composite key.

## alias

If your business key columns have different names across the different tables, they will need to be aliased to the same name.

## business_definition

A satellite is named by combining source system, business definition and version. It is useful when attributes of a business are split into multiple satellites.

## payload

List of business_topic attributes represented by column names and relevant data types.

# Raw vault objects

## HUB

It is a uniquely identifiable business element. It has the semantic meaning accross the business and same granularity.

## SATELLITE

It represents descriptive attributes of a business key/business element at a point in time. i.e. customer name, customer date of birth.

## LINK

It is a uniquely identifiable relationship between business elements(Hubs) and represents an unit of work(process/activity) or hierarchy.

## Set creation of hubs, links and sats in the schema of choice

By detault all the artefacts would be created in public schema. You can overide it in the specific model, by adding following lines at the start-
e.g. hub customers.sql

    {{ config(materialized='incremental',
    schema = "SATS"
    ) }}
Note the above line of code is automatically added to the artefact files. Also add custom schema macro called get_custom_schema.sql to the macros directory. This will ensure artefacts are created in your schema of choice.

## Staging, Hubs, Links, Sats

Set staging models to views in the dbt_project.yml as below-

    models:
    +transient: false
    autovault:
        # Applies to all files under models/example/
        stage:
            materialized: view

To compute the incremental update in the hubs, links and satellites, dbt will calculate hash of the business keys and hashdiff of payload columns which can ve expensive as it happens multiple times for each hub, link and satellite related to a source table. If performance is as issue the staging layer that feeds the raw vault can be materialised as table. There is a trade of between cost of materialising the staging layer and speed and the compute cost if it relies on virtualised staging layer.
To materialise staging layer as a table, update the staging template - generate_raw_vault/app/templates/staging_model.sql with following lines:

    {{
    config(materialized='table',
    schema = "STAGING"
    ) }}

## Raw Vault Rules

The unit of work is the foundation of forming hubs and links; the business process must be preserved to have a full audit trail of the source data into the raw vault - you should be able to recreate the original source and business process from it.

Write the metadata file with the hubs in order of the unit of work - the business key hierarchy must be maintained; the business key in the first hub will become the driving key.

- Each business topic corresponds to a unique hub.
- A link connects all business topics, to avoid breaking relationship between multiple business topics that preserves the unit of work (business process/activity) which is useful for optimisation and lineage.
- ource data must include a timestamp of when the record was produced; updates are seen as a new piece of data that is produced and so must also include a created timestamp. The timestamp is used in the append only raw vault to filter to the latest record or state of any given process.
- Payload columns can only be persisted to satellites which retains their business context, if the context is lost it is in the wrong satellite e.g. Party role agreements only makes sense when the role is attached to the agreement, detaching the two breaks the business logic continuity.
- If the source data has a business topic which does not have any related business keys, the record will only be populated in the hub and link table preserving the lineage and connection to other business hubs and satellites within said data.

# Running the project

## Sample data

Sample data can be found in the `./data` and their schemas can be found in `./sample_data_schema`. The sample data will create 3 hubs, 1 link and multiple satellites.

## Generating the raw vault

To ingest sample data in the snowflake public schema, run command:

    dbt seed

To generate dbt raw vault model files ensure you have create the metadata file `./source_metadata`; metadata files for example source data have been provided. Run the command:

    python3 ./generate_raw_vault/app/main.py

Note: If you get a ModuleNotFoundError then the folder directory may need to be added to your PYTHONPATH environment variable with the appropriate command below. Alternatively, you can update this in your .zshrc file.

**For UNIX (Linux, OSX, ...)**

```python
export PYTHONPATH=“${PYTHONPATH}:/path/to/your/project/”
```

**For Windows**

```python
set PYTHONPATH=%PYTHONPATH%;C:\path\to\your\project\
```

To deploy the model in snowflake run command:

    dbt run

Raw vault artefacts would be created in the target database.

## Name dictionary

Database name and system directory often have character length limits. The naming convention dictionary has been included to standardise shortened naming for models. This can be found in `./name_dictionary`; add more key value name conventions as required that will be used in link creation.

## Contributing

Code can be merged into the current development branch main by opening a pull request (PR). For public users, these pull requests will need to be created from your own fork of the repository.

An IW repository maintainer will review your PR. They may suggest code revision for style or clarity, or request that you add unit or integration test(s).

### Resources

- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](http://slack.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best
