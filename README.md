# dbtvault practice
Install Snowsql

    brew install snowflake-snowsql

Run snowsql to install the cli; if the cmd is not recognised then add snowsql to your path. To add snowsql to the path on mac, add the following to your .zshrc file. If .zshrc file does not exist run:

    touch .zshrc
    export PATH=/Applications/SnowSQL.app/Contents/MacOS:$PATH

## setting up snowsql cli
Populate the the snowsql config file with connection details of your snowflake a/c and update the options particularly for the log file location.
example-

    [connections.iw]
    accountname = infinityworkspartner
    region = eu-west-1
    role = infra_builder
    username = kiran.bhat@infinityworks.com
    warehouse = demo_wh
    private_key_path = /Users/kiran.bhat/.ssh/snowsql/rsa_key.p8

    [variables]
    # SnowSQL defines the variables in this section on startup.
    # You can use these variables in SQL statements. For details, see
    # https://docs.snowflake.com/en/user-guide/snowsql-use.html#using-variables

    # example_variable=27

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

## authenticate snowsql connection
This project uses rsa keys as secure methods for authentication. To generate a private key edit and run the following cmd

    mkdir -p ~/.ssh/snowsql
    openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out ~/.ssh/snowsql/rsa_key.p8
This will prompt you for a password to encrypt the private key. To keep passphrase safe and for convenience, to decrypt the key include it in the .zshrc file

    export SNOWSQL_PRIVATE_KEY_PASSPHRASE=

Create you public key using the private key using the following cmd-

    openssl rsa -in  ~/.ssh/snowsql/rsa_key.p8 -pubout -out ~/.ssh/snowsql/rsa_key.pub

To test the connection run the snowsql cmd to your desired profile e.g. `connections.iw`

        snowsql --connection  iw
        !exit

# Install DBT
select a directory to install dbt or create a new directory

    mkdir dbtpractice (e.g.)

Create a virtual environment; standard convnetion of a virtual env is .venv

    python3 -m venv .venv

Activate the environment

    source .venv/bin/activate

Install DBT

    pip3 install dbt==x.x.x (latest version)

Create and configure DBT project e.g. prj_xx

    dbt init  prj_xx --adapter snowflake

# Configure connection to snowflake
Edit profile.yml ~/.dbt/profiles.yml

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

Test DBT connection

    dbt debug

# Install dbtvault
Refer link - https://hub.getdbt.com/datavault-uk/dbtvault/latest/

# Load sample source data into snowflake and set data sources for the project
Create raw data tables using following DDLs-

    CREATE  OR REPLACE TABLE "AUTOVAULT"."PUBLIC".TRANSACTIONS (TRSACTION VARIANT, RECORD_SOURCE STRING, LOAD_DATE TIMESTAMP_NTZ);

    CREATE OR REPLACE TABLE "AUTOVAULT"."PUBLIC".CUSTOMERS (CUSTOMER_ID STRING, AVG_VISITS_PER_MONTH NUMBER, RECORD_SOURCE STRING, LOAD_DATE TIMESTAMP_NTZ);

    CREATE OR REPLACE TABLE "AUTOVAULT"."PUBLIC".PRODUCTS (PRODUCT_ID STRING, MODEL STRING, MAKE STRING, RECORD_SOURCE STRING, LOAD_DATE TIMESTAMP_NTZ);

    CREATE OR REPLACE TABLE "AUTOVAULT"."PUBLIC".CUSTOMER_VISITS (CUSTOMER_ID STRING, MONTHLY_VISITS_AVG NUMBER, RECORD_SOURCE STRING, LOAD_DATE TIMESTAMP_NTZ);

    CREATE OR REPLACE TABLE "AUTOVAULT"."PUBLIC".TOTAL_CUST_VISITS (CUST_ID STRING, TOTAL_VISITS NUMBER, RECORD_SOURCE STRING, LOAD_DATE TIMESTAMP_NTZ);

Load it to internal user stage in snowflake via snowsql CLI. Note- you cannot use this in Snowflake console hence the CLI. Simlilarly load other data sets.
e.g.

    put file://~/documents/datavault/snowflake101/customers.csv @~/staged AUTO_COMPRESS = FALSE

    put file:///yourfilelocation @~/staged AUTO_COMPRESS = FALSE

Copy  data from internal snoflake stage to the table
e.g.

    COPY INTO "mydb"."myschema"."PRODUCTS" FROM (SELECT $1, $2, $3, 'PRODUCTS',TO_TIMESTAMP_NTZ(CURRENT_TIMESTAMP) FROM '@~/staged/products.csv') file_format = (format_name = 'myCSV');

## Set data sources
Add following lines to the schema.yml file found under models directory.

    version: 2
    sources:
    - name: AV (custom name)
        database: AUTOVAULT (your snowflake database)
        schema: PUBLIC (your scheme under)
        tables:
        - name: CUSTOMERS
        - name: PRODUCTS
        - name: TRANSACTIONS
        - name: CUSTOMER_VISITS
        - name: TOTAL_CUST_VISITS

## Flatten transcations data with json records
flatten_transactions.sql flattens the transactions data using latteral flatten sql command.

# Set creation of hubs, links and sats in the schema of choice
By detault all the artefacts would be created in public schema. You can overide it in the specific model, by adding following lines at the start-
e.g. hub customers.sql

    {{ config(materialized='incremental',
    schema = "SATS"
    ) }}

Also add custom schema macro called get_custom_schema.sql to the macros directory. This will ensure artefacts are created in your schema of choice.

# Staging, Hubs, Links, Sats
Set staging models to views in the dbt_project.yml as below-

    models:
    +transient: false
    autovault:
        # Applies to all files under models/example/
        stage:
            materialized: view

Stage sample data as views by creating staging models, under folder called stage under models directory, that add meta data to the source i.e. load_date, effective_from date, primary key hash, hashdiff etc.
e.g. stg_customers.sql. Copy model from final model section of the following dbtvault doc. Update it to suit your project.
https://dbtvault.readthedocs.io/en/latest/tutorial/tut_staging/

## Hubs
Create Hub tables from the stating views. Refer dbtvault doc link - https://dbtvault.readthedocs.io/en/latest/tutorial/tut_hubs/
Copy hub template from this link. E.g. customers.sql model under hub directory. Update it to suit your project.
If your primary key and natural key columns have different names across the different tables, they will need to be aliased to the same name in the respective staging layers via a derived column configuration, using the stage macro in the staging layer.
e.g. stg_total_cust_visits.sql

derived_columns:
CUSTOMER_ID: "CUST_ID" (total_cust_visits source dataset has natural key column called 'cust_id' that is different to the other data sources with column name as 'customer_id))

## Links
Create Link tables from the stating views. Refer dbtvault doc link - https://dbtvault.readthedocs.io/en/latest/tutorial/tut_links/
Copy link template from this doc link. E.g. customer_prod.sql model under links directory. Update it to suit your project.

## Sats
Create satellite tables from the stating views. Refer dbtvault doc link - https://dbtvault.readthedocs.io/en/latest/tutorial/tut_satellites/
Copy satellite template from this doc link. E.g. customer.sql model under sats directory. Update it to suit your project.

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](http://slack.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
