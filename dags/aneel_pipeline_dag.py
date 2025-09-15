from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.docker.operators.docker import DockerOperator

# This DAG defines the automated E(L)T pipeline for the ANEEL MMGD dataset.
#
# The pipeline consists of two main steps:
# 1. Wait for the raw data file to appear in the MinIO landing-zone.
# 2. Run the dbt project to transform the raw data into staging and mart models.
#
# The dbt tasks are executed using the DockerOperator, which runs dbt inside a
# self-contained container using the image defined in dbt/Dockerfile.

with DAG(
    dag_id="aneel_mmgd_pipeline",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    doc_md="""
    ### ANEEL MMGD Data Pipeline

    This DAG orchestrates the transformation of the ANEEL MMGD dataset.

    **Setup Requirements:**
    1.  **Airflow Connection:** Create an S3 connection named `minio_s3_connection` in the Airflow UI.
        -   **Connection Type:** Amazon S3
        -   **Extra:** `{"host": "http://datalake:9000", "aws_access_key_id": "minioadmin", "aws_secret_access_key": "minioadmin"}`
    2.  **Airflow Variables:** Create the following Airflow Variables:
        -   `DBT_TRINO_HOST`: `trino-coordinator`
        -   `MINIO_ROOT_USER`: `minioadmin`
        -   `MINIO_ROOT_PASSWORD`: `minioadmin`

    **Pipeline Steps:**
    - It waits for the raw data file (`dados_aneel.csv`) in the `landing-zone` bucket in MinIO.
    - It uses dbt via the DockerOperator to build the data models (runs models and tests).
    """,
    tags=["data-engineering", "dbt", "trino"],
) as dag:

    # Task 1: Wait for the raw data file in MinIO
    wait_for_raw_data = S3KeySensor(
        task_id="wait_for_raw_data_file",
        bucket_name="landing-zone",
        bucket_key="dados_aneel.csv",
        aws_conn_id="minio_s3_connection",
        mode="poke",
        poke_interval=60,
        timeout=1800, # Wait for 30 minutes
    )

    # Task 2: Run the dbt project using the DockerOperator
    run_dbt_build = DockerOperator(
        task_id="run_dbt_build",
        image="aneel-pipeline/dbt:latest",
        command="build", # 'dbt build' runs models and tests
        auto_remove=True,
        # The dbt container needs to connect to the same network as Trino and MinIO
        network_mode="datalakehouse",
        # Pass environment variables to the container.
        # The dbt profiles.yml is configured to read these variables.
        environment={
            "DBT_TRINO_HOST": "{{ var.value.DBT_TRINO_HOST }}",
            "MINIO_ROOT_USER": "{{ var.value.MINIO_ROOT_USER }}",
            "MINIO_ROOT_PASSWORD": "{{ var.value.MINIO_ROOT_PASSWORD }}",
        },
    )

    # Define the task dependency
    wait_for_raw_data >> run_dbt_build
