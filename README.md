# Airbnb ETL Pipeline

This repository contains a PySpark-based ETL pipeline for Airbnb listing data and an Apache Airflow orchestration layer that can be run locally via Docker.

## Prerequisites

- Docker Desktop or Docker Engine 20+
- Docker Compose V2 (shipped with Docker Desktop)
- Python 3.9+ (optional, for local execution outside Docker)

## Directory Layout

- `src/`: PySpark ETL code (`extract.py`, `transform.py`)
- `dags/`: Airflow DAGs (`airbnb_etl_dag.py`)
- `data/`: Input and output data directories mounted inside Airflow containers
- `sql/`: Optional SQL resources mounted inside Airflow containers
- `logs/`, `plugins/`: Airflow runtime directories (created automatically if missing)
- `docker-compose.yaml`: Docker Compose definition for the Airflow stack
- `Dockerfile`: Custom Airflow image with PySpark dependencies

## Quick Start

1. **Create the Airflow environment file**

   Use `.env.example` as a reference and create an `.env` file with your local UID while forcing `AIRFLOW_GID=0` (required by the official Airflow image). On macOS/Linux you can run:

   ```bash
   printf "AIRFLOW_UID=%s\nAIRFLOW_GID=0\n" "$(id -u)" > .env
   ```

2. **Bootstrap the Airflow metadata database and admin user**

   ```bash
   docker compose up airflow-init
   ```

3. **Start the Airflow webserver and scheduler**

   ```bash
   docker compose up -d
   ```

4. **Access the web UI**

   - URL: http://localhost:8080
   - Username: `admin`
   - Password: `admin`

5. **Trigger the ETL DAG**

   - In the UI, activate and trigger the `airbnb_etl_pipeline` DAG.
   - The DAG invokes `src.transform.transform_airbnb_data`, writing cleaned Parquet data to `data/processed/` inside the mounted volume.

## Custom Image Details

The custom Airflow image installs OpenJDK 17 and project-specific Python packages (PySpark, Google BigQuery client, plotting libraries) so that Spark jobs can run inside the Airflow tasks. The `PYTHONPATH` environment variable in `docker-compose.yaml` exposes the `src/` directory to all Airflow components.

## Data Locations

The `data/` directory is mounted at `/opt/airflow/data` in every container. Ensure raw CSV data is available in `data/raw/` before triggering the DAG. Transformed parquet outputs are written to `data/processed/`.

## Stopping and Cleaning Up

- Stop services: `docker compose down`
- Stop and remove volumes (including the Postgres metadata database):

  ```bash
  docker compose down --volumes
  ```

## Troubleshooting

- Rebuild the image after dependency changes: `docker compose build`
- Reset the Airflow metadata database: remove the `postgres-db-volume` via `docker volume rm airbnb_etl_pipeline_postgres-db-volume`
- Inspect service logs: `docker compose logs -f airflow-webserver`

# airbnb_etl_pipeline
