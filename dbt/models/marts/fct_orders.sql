with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

final as (
    select
        o.order_id,
        o.order_date,
        o.order_status,
        o.quantity,
        o.unit_price,
        o.total_amount,
        o.campaign_id,

        -- customer info
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.country,
        c.city,

        -- product info
        p.product_id,
        p.product_name,
        p.category

    from orders o
    left join customers c using (customer_id)
    left join products p using (product_id)
)

select * from final