with source as (
    select * from {{ ref('raw_customers') }}
),

renamed as (
    select
        customer_id,
        first_name,
        last_name,
        lower(trim(email))               as email,
        initcap(country)                 as country,
        initcap(city)                    as city,
        cast(signup_date as date)        as signup_date
    from source
    where customer_id is not null
      and email is not null
)

select * from renamed