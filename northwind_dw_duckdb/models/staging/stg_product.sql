with source as(
   select * 
   from {{ source('northwind', 'products') }}
   where supplier_ids not like '%;%'
)
    
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source