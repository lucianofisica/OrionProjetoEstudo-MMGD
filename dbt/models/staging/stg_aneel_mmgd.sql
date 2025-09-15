-- This staging model cleans and standardizes the raw MMGD data from the bronze layer.
-- It performs the following transformations:
-- 1. Renames columns to a consistent and readable format.
-- 2. Casts columns to their appropriate data types (e.g., numbers, dates).
-- 3. Replaces decimal commas with decimal points for numeric conversion.
-- 4. Filters out records with null essential identifiers, similar to the logic in the original notebook.

with source as (
    -- Source data from the raw external table
    select * from {{ source('bronze', 'mmgd_aneel_raw') }}
),

renamed_and_casted as (
    select
        -- Identifiers
        "CodGeracaoDistribuida" as codigo_unidade_geradora,

        -- Timestamps
        -- Cast the connection date string to a proper DATE type
        cast(from_iso8601_timestamp("DatConexao") as date) as data_conexao,
        cast(from_iso8601_timestamp("DatGeracaoConjuntoDados") as date) as data_geracao_dados,

        -- Numeric Values
        -- The data uses a comma as a decimal separator, so we replace it with a dot
        -- before casting to DOUBLE. We also handle potential nulls.
        try_cast(replace("MdaAreaArranjo", ',', '.') as double) as area_arranjo_m2,
        try_cast(replace("MdaPotenciaInstalada", ',', '.') as double) as potencia_instalada_kw,
        try_cast(replace("MdaPotenciaModulos", ',', '.') as double) as potencia_modulos_kw,
        try_cast(replace("MdaPotenciaInversores", ',', '.') as double) as potencia_inversores_kw,
        "QtdModulos" as quantidade_modulos,

        -- Categorical Information (Manufacturers and Models)
        -- We can apply upper() and trim() to standardize the text data
        trim(upper("NomFabricanteModulo")) as fabricante_modulo,
        trim(upper("NomFabricanteInversor")) as fabricante_inversor,
        trim(upper("NomModeloModulo")) as modelo_modulo,
        trim(upper("NomModeloInversor")) as modelo_inversor

    from source
)

-- Final selection and filtering
select
    *
from renamed_and_casted
where
    -- This clause replicates the `dropna()` logic from the original notebook,
    -- ensuring that key fields required for analysis are present.
    codigo_unidade_geradora is not null
    and data_conexao is not null
    and potencia_instalada_kw is not null
    and fabricante_modulo is not null
    and fabricante_inversor is not null
