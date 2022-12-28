{% docs customers_v0_1_0_table_desc %}

# CUSTOMERS_V0_1_0
This table contains data describing a customer.

The original business process that generated the data is: CUST_STATS

## Source
- Name: CUSTOMERS
- Version: 0_1_0
- System: CRM_SYSTEM
- Freshness: Updated daily at 5am
- Format: Flat
- Filetype: .csv

## Accessibility
- Raw source location: s3://data-lake-dev/customers
- Warehouse location: https://instance.eu-west-1.snowflakecomputing.com/console
- Warehouse role access: "DATA_ANALYST", "DATA_SCIENTIST"

### Access requests
Contact the Data squad for Snowflake and table access

#### Maintained by
Data set maintained by: Data squad

## Quality & Known Issues
This file often has null primary keys
{% enddocs %}
