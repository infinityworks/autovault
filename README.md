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

# Load sample data
Load it to internal user stage in snowflake via snowsql CLI. Note- you cannot use this in Snowflake console hence the CLI. Simlilarly load other data sets.
e.g. put file://~/documents/datavault/snowflake101/customers.csv @~/staged AUTO_COMPRESS = FALSE

put file:///yourfilelocation @~/staged AUTO_COMPRESS = FALSE

Copy  data from internal snoflake stage to the table
e.g. COPY INTO "mydb"."myschema"."PRODUCTS" FROM (SELECT $1, $2, $3, 'PRODUCTS',TO_TIMESTAMP_NTZ(CURRENT_TIMESTAMP) FROM '@~/staged/products.csv') file_format = (format_name = 'myCSV');

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
