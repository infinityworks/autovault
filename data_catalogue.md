
# Customers
This data lists customers' average monthly visits
    Natural  Key:
        CUSTOMER_ID
    Payload columns:
        AVG_MONTHLY_VISITS

# Customer Visits
This data lists customers' total visits for new customers not already in the Customers dataset above
    Nataural Key:
        CUSTOMER_ID
    Payload columns:
        TOTAL_VISITS

# Total Customer Visits
This data lists customers' total visits with natural key column name different to other sources
    Nataural Key:
        CUST_ID
    Payload columns:
        TOTAL_VISITS

# Products
This data lists all products
    Natural Key:
        PRODUCT_ID
    Payload columns:
        MAKE
        MODEL

# Transactions
This data lists all products viewed by customers by datetime in json format and must be flattened
    Payload Columns:
        CUSTOMER_ID
        DATE_OF_SESSION
        PRODUCTS_VIEWED
            PRICE
            PRODUCT_ID
