-- This mart model aggregates the cleaned staging data to provide business insights.
-- It calculates the total installed power and the count of generation units
-- for each module manufacturer.
-- This table is suitable for direct use in BI tools like Superset or Metabase.

with staging_data as (
    -- Reference the cleaned staging model
    select
        fabricante_modulo,
        potencia_instalada_kw
    from {{ ref('stg_aneel_mmgd') }}
    where
        fabricante_modulo is not null
        and potencia_instalada_kw > 0
)

select
    fabricante_modulo,

    -- Sum of installed power for each manufacturer
    sum(potencia_instalada_kw) as potencia_total_instalada_kw,

    -- Count of distinct generation units for each manufacturer
    count(*) as total_unidades_geradoras,

    -- Average power per unit
    avg(potencia_instalada_kw) as potencia_media_por_unidade_kw

from staging_data
group by
    fabricante_modulo
order by
    potencia_total_instalada_kw desc
