with source as (
    select * from {{ ref('raw_products') }}
),

renamed as (
    select
        product_id,
        product_name,
        initcap(category)                as category,
        cast(price as numeric)           as price,
        cast(stock_quantity as int64)    as stock_quantity
    from source
    where product_id is not null
)

select * from renamed