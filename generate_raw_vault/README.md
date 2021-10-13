# Generate Raw Vault

This project creates the raw vault concepts, physicalising Hubs, Links and Satellites.

## Metadata

The raw vault generator creates dbt `.sql` files which create tables and views in the data warehouse; it creates these from metadata files in JSON format, located in `source_metadata/` which describe the business topics, business definitions and keys of a data set. The output will be `.sql`  files which create Hubs, links and satellites.

The metadata used in generating the files is defined by the data producer, the metadata is different to that which the package [dbtvault](https://dbtvault.readthedocs.io/en/latest/) uses.

## Running the project

To run the project, execute.

```
python3 generate_raw_vault/app/main.py
```
