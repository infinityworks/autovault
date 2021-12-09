# Sample data schema

## Customers
This data lists customers' average monthly visits
    Primary Key:
        CUSTOMER_ID
    Payload columns:
        AVG_MONTHLY_VISITS
        RECORD_SOURCE
        LOAD_DATETIME
## Total Customer Visits
This data lists customers' total visits
    Primary Key:
        CUSTOMER_ID
    Payload columns:
        TOTAL_VISITS
        RECORD_SOURCE
        LOAD_DATETIME
## Products
This data lists all products
    Primary Key:
        PRODUCT_ID
    Payload columns:
        MAKE
        MODEL
        RECORD_SOURCE
        LOAD_DATETIME
## Transactions
This data lists all products viewed by customers by datetime
    Primary Key:
        DATE_OF_SESSION
    Payload Columns:
        CUSTOMER_ID
        PRODUCT_ID
        PRICE
        RECORD_SOURCE
        LOAD_DATETIME
