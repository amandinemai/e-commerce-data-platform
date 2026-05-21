with orders as (
    select * from {{ ref('fct_orders') }}
    where order_status = 'completed'
),

final as (
    select
        order_date,
        country,
        category,
        campaign_id,
        count(distinct order_id)            as total_orders,
        sum(total_amount)                   as total_revenue,
        avg(total_amount)                   as avg_order_value,
        count(distinct customer_id)         as unique_customers
    from orders
    group by 1, 2, 3, 4
)

select * from final