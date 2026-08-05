# DW_lab1_6630202670
for test in class (hope i can pass)

## Folder Structure of northwind_dw_duckdb

```text
northwind_dw_duckdb/
├── analyses/
│   └── .gitkeep
├── macros/
│   └── .gitkeep
├── models/
│   └── example/
│       ├── my_first_dbt_model.sql
│       ├── my_second_dbt_model.sql
│       └── schema.yml
├── seeds/
│   └── .gitkeep
├── snapshots/
│   └── .gitkeep
├── tests/
│   └── .gitkeep
├── .gitignore
├── README.md
├── dbt_project.yml
└── dev.duckdb
```
- dim_products: load data from stg_products, join supplier information from stg_suppliers, rename id to product_id, deduplicate records by product_id using row_number(), and insert insertion timestamp.
- dim_date: create the date dimension from 2014-01-01 to 2050-01-01 using GENERATE_DATE_ARRAY, create id as the formatted date key in YYYY-MM-DD, derive full_date, year, year_week, year_day, fiscal_year, fiscal_qtr, month, month_name, week_day, day_name, and day_is_weekday, and include all rows for each calendar date.
- fact_sales: combine order and order detail data from stg_orders and stg_order_details, join on order_id, include sales facts such as quantity, unit_price, discount, dates, and insertion timestamp, and deduplicate records by customer_id, employee_id, order_id, product_id, shipper_id, purchase_order_id, and order_date using row_number().