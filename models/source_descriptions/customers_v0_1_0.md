{% docs customers_v0_1_0_desc %}

# CUSTOMERS_V0_1_0
This table contains data describing a customer.

The original business process that generated the data is: CUST_STATS

## Source
- Name: CUSTOMERS
- Version: 0.1.0
- System: CRM_SYSTEM
- Freshness: Updated daily at 5am
- Format: Flat
- Filetype: .csv

## Accessibility
- Raw source location: s3://data-lake-dev/customers
- Database location: https://instance.eu-west-1.snowflakecomputing.com/console
- Database role access: "data_analyst", "data_scientist"

### Access requests
Contact the Data squad for Snowflake and table access.

## Quality
This file often has null primary keys
{% enddocs %}

{% docs customers_v0_1_0_col_customer_id %}
This is the driving key, a unique identifier to represent a customer.
{% enddocs %}

{% docs customers_v0_1_0_col_age %}
The customers age in years
{% enddocs %}
