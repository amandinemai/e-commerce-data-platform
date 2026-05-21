with source as (
    select * from {{ ref('raw_orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        product_id,
        campaign_id,
        cast(quantity as int64)          as quantity,
        cast(unit_price as numeric)      as unit_price,
        cast(total_amount as numeric)    as total_amount,
        lower(trim(order_status))        as order_status,
        cast(order_date as date)         as order_date
    from source
    where order_id is not null
)

select * from renamed