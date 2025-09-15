import os
import duckdb
import pandas as pd
from dotenv import load_dotenv

# This script performs an initial exploration of the raw data stored in MinIO.
# It uses DuckDB to directly query the CSV file from the S3-compatible storage.

def explore_raw_data():
    """
    Connects to MinIO, reads the raw ANEEL dataset using DuckDB,
    and prints exploratory information.
    """
    # Load environment variables from a .env file
    load_dotenv()

    # --- Configuration ---
    minio_endpoint = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    minio_access_key = os.getenv("MINIO_ROOT_USER", "minioadmin")
    minio_secret_key = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")

    # The name of the raw data file. Assumes the user has uploaded it.
    # This should be the actual name of the ANEEL dataset file.
    # We'll use 'dados_aneel.csv' as a placeholder name.
    raw_data_filename = "dados_aneel.csv"
    landing_bucket = "landing-zone"
    s3_path = f"s3://{landing_bucket}/{raw_data_filename}"

    print("--- Initializing Data Exploration ---")
    print(f"Attempting to connect to MinIO at: {minio_endpoint}")
    print(f"Querying data from: {s3_path}\n")

    try:
        # --- Connect to DuckDB and Configure S3 Access ---
        con = duckdb.connect(database=':memory:', read_only=False)

        # Install and load the httpfs extension to read from S3
        con.execute("INSTALL httpfs;")
        con.execute("LOAD httpfs;")

        # Configure S3 provider and credentials
        con.execute(f"SET s3_endpoint = '{minio_endpoint.replace('http://', '')}';")
        con.execute("SET s3_url_style = 'path';")
        con.execute("SET s3_use_ssl = false;")
        con.execute(f"SET s3_access_key_id = '{minio_access_key}';")
        con.execute(f"SET s3_secret_access_key = '{minio_secret_key}';")

        # --- Query the Data ---
        # DuckDB can directly query CSV files from S3.
        # We use 'read_csv_auto' to infer columns and types.
        # LIMIT 1000 to avoid loading the entire 3.6M rows for a quick exploration.
        query = f"""
        SELECT *
        FROM read_csv_auto('{s3_path}', SAMPLE_SIZE=20000)
        LIMIT 1000;
        """

        print("Executing query to fetch a sample of the data...")
        df_sample = con.execute(query).fetchdf()

        # --- Display Exploratory Information ---
        print("\n--- Data Exploration Results ---")

        print("\n1. Data Sample (First 5 Rows):")
        print(df_sample.head())

        print("\n2. DataFrame Info (Columns, Types, Non-null counts):")
        # Create a string buffer to capture the output of df.info()
        from io import StringIO
        info_buf = StringIO()
        df_sample.info(buf=info_buf)
        print(info_buf.getvalue())

        print("\n3. Basic Statistics:")
        # The describe output can be wide, so we adjust pandas display options
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
            print(df_sample.describe(include='all').transpose())

        # --- Query for total row count ---
        print("\n4. Total Row Count (from source file):")
        total_rows_query = f"SELECT COUNT(*) FROM read_csv_auto('{s3_path}');"
        total_rows = con.execute(total_rows_query).fetchone()[0]
        print(f"The raw data file contains {total_rows:,} rows.")

        print("\n--- Exploration Complete ---")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check the following:")
        print("1. Is Docker with the 'datalake' service running?")
        print(f"2. Has the data file '{raw_data_filename}' been uploaded to the '{landing_bucket}' bucket in MinIO?")
        print("3. Are the MinIO credentials and endpoint in your .env file correct?")

    finally:
        if 'con' in locals():
            con.close()

if __name__ == "__main__":
    explore_raw_data()
