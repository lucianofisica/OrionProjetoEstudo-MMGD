import os
from trino.dbapi import connect
from trino.auth import BasicAuthentication
from dotenv import load_dotenv

# This script creates an external table in the Hive Metastore via Trino.
# The table points to the raw CSV data stored in the MinIO landing-zone.
# This makes the raw data queryable through SQL.

def create_external_table():
    """
    Connects to Trino and creates a schema and an external table for the raw data.
    """
    load_dotenv()

    # --- Configuration ---
    trino_host = os.getenv("TRINO_HOST", "localhost")
    trino_port = int(os.getenv("TRINO_PORT", 8080))
    trino_user = os.getenv("TRINO_USER", "admin") # Trino user can be anything

    # Assumes the raw data file has this name in the landing-zone
    raw_data_filename = "dados_aneel.csv"
    landing_bucket = "landing-zone"
    s3_path = f"s3a://{landing_bucket}/" # Note: s3a protocol for Hive

    catalog = "hive"
    schema = "bronze" # Raw data layer
    table_name = "mmgd_aneel_raw"

    print("--- Starting Metadata Registration ---")
    print(f"Connecting to Trino at: {trino_host}:{trino_port}")

    try:
        # --- Connect to Trino ---
        conn = connect(
            host=trino_host,
            port=trino_port,
            user=trino_user,
        )
        cur = conn.cursor()
        print("Successfully connected to Trino.\n")

        # --- Create Schema (Database) ---
        # The schema is created in the 'hive' catalog, which points to MinIO.
        create_schema_sql = f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}"
        print(f"Executing: {create_schema_sql}")
        cur.execute(create_schema_sql)
        print(f"Schema '{schema}' created or already exists.\n")

        # --- Create External Table ---
        # This table definition is based on the README.md documentation.
        # It's an EXTERNAL table, so Trino/Hive manage the metadata, but the
        # data itself remains in the CSV file in MinIO.
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {catalog}.{schema}.{table_name} (
            _id BIGINT,
            DatGeracaoConjuntoDados VARCHAR,
            CodGeracaoDistribuida VARCHAR,
            MdaAreaArranjo VARCHAR,
            MdaPotenciaInstalada VARCHAR,
            NomFabricanteModulo VARCHAR,
            NomFabricanteInversor VARCHAR,
            DatConexao VARCHAR,
            MdaPotenciaModulos VARCHAR,
            MdaPotenciaInversores VARCHAR,
            QtdModulos BIGINT,
            NomModeloModulo VARCHAR,
            NomModeloInversor VARCHAR
        )
        WITH (
            format = 'CSV',
            skip_header_row = true,
            external_location = '{s3_path}'
        )
        """

        print(f"Executing CREATE TABLE statement for '{table_name}'...")
        # A bit of formatting to make the printed SQL readable
        print("SQL Statement:\n" + "".join([line.strip() + "\n" for line in create_table_sql.strip().split('\n')]))

        cur.execute(create_table_sql)
        print(f"Table '{table_name}' created successfully in schema '{schema}'.")
        print("This table now points to the raw CSV data in MinIO.")

        print("\n--- Metadata Registration Complete ---")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check the following:")
        print("1. Are all Docker services running (`docker-compose ps`)?")
        print("2. Is Trino healthy and accessible at the configured host/port?")
        print(f"3. Has the data file '{raw_data_filename}' been uploaded to the '{landing_bucket}' bucket in MinIO?")

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_external_table()
