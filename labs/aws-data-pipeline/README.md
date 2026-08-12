# AWS Data Engineering Lab

Hands-on data engineering lab built to demonstrate AWS-oriented backend and analytics skills with both a real-AWS design and a local AWS-compatible execution path.

## Goal

Build a small data lake pipeline that:

1. Uploads raw CSV data to S3 with Python/Boto3.
2. Catalogs the dataset with AWS Glue Data Catalog.
3. Transforms sales data with PySpark.
4. Writes a curated Parquet layer.
5. Queries the curated data with Athena SQL.
6. Defines infrastructure with Terraform.

## Architecture

```text
                         AWS design

Local CSV
   |
   | Python + Boto3
   v
S3 raw/ ---------> Glue Crawler ---------> Glue Data Catalog
   |                                        |
   |                                        v
   +-------------> Glue PySpark Job ----> S3 curated/
                                              |
                                              v
                                            Athena
```

## Local AWS simulation with Floci

The lab also has an executable local path using Floci on port `4566`.

```text
CSV
 |
 | Boto3
 v
Floci S3 raw/
 |
 | local PySpark container
 v
Floci S3 curated/ (Parquet)
 |
 +------> Floci Glue Data Catalog
             |
             v
       Floci Athena + DuckDB
             |
             v
         SQL results
```

Floci currently emulates the Glue **Data Catalog** but not the managed Glue Crawler or Glue Job runtime. For that reason the local path deliberately does two things:

- Runs the transformation with real PySpark in a local Docker container.
- Registers the raw and curated table metadata directly in the Glue Data Catalog.

The AWS-oriented files remain in `glue/` and `terraform/` to show how the same workload maps to managed AWS services.

## Skills demonstrated

- Python
- Boto3
- AWS S3
- AWS Glue Data Catalog
- AWS Glue Jobs design
- AWS Glue Crawlers design
- PySpark
- Parquet
- Amazon Athena
- SQL
- Terraform
- IAM
- Docker
- Git

## Repository structure

```text
labs/aws-data-pipeline/
├── docker-compose.floci.yml
├── local/
│   ├── Dockerfile
│   ├── requirements-local.txt
│   └── run_local_pipeline.py
├── python/
│   ├── run_glue_job.py
│   └── upload_to_s3.py
├── glue/
│   └── transform_sales.py
├── sample/
│   └── sales.csv
├── sql/
│   └── analytics.sql
├── terraform/
│   └── main.tf
├── terraform-floci/
│   └── main.tf
└── requirements.txt
```

## Run the complete lab locally

Requirements:

- Docker Desktop / Docker Engine
- Docker Compose

From this directory:

```bash
docker compose -f docker-compose.floci.yml up -d floci
docker compose -f docker-compose.floci.yml run --rm pipeline
```

The pipeline will:

1. Wait for Floci.
2. Create the local S3 bucket.
3. Upload `sample/sales.csv` with Boto3.
4. Transform the CSV with PySpark.
5. Upload curated Parquet data to S3.
6. Register `raw_sales` and `curated_sales` in Glue Data Catalog.
7. Run a real Athena-style SQL query through Floci/DuckDB.
8. Print the query result and final S3 objects.

Stop the environment:

```bash
docker compose -f docker-compose.floci.yml down
```

## Optional: provision local resources with Terraform

With Floci running:

```bash
cd terraform-floci
terraform init
terraform apply -auto-approve
cd ..
docker compose -f docker-compose.floci.yml run --rm pipeline
```

The Terraform configuration points the AWS provider to `http://localhost:4566`, so no real AWS credentials or cloud account are required for this local mode.

## Example dataset

```text
order_id,customer_id,product,quantity,unit_price,order_date
1001,C001,Keyboard,1,45.90,2026-08-01
1002,C002,Mouse,2,19.90,2026-08-01
1003,C001,Monitor,1,219.00,2026-08-02
```

## Real AWS path

The repository keeps a separate AWS implementation path:

- `python/upload_to_s3.py`: raw ingestion with Boto3.
- `python/run_glue_job.py`: Glue Job launcher using Boto3.
- `glue/transform_sales.py`: Glue-compatible PySpark ETL.
- `terraform/main.tf`: AWS infrastructure baseline.
- `sql/analytics.sql`: analytics queries.

Do not treat the local Floci run as proof of a production AWS deployment. It is an AWS-compatible local integration lab designed to validate the data flow, SDK calls, catalog metadata, PySpark transformations and Athena queries without cloud cost.

## Interview talking points

- Why raw CSV and curated Parquet are separated.
- How Boto3 clients change between local emulation and AWS endpoints.
- Why a Glue Crawler is useful in AWS and why the local path registers metadata directly.
- How PySpark transforms and enriches the dataset.
- Why IAM permissions should be scoped to the specific bucket and prefixes.
- How Terraform makes the infrastructure reproducible.
- What would change before using this architecture in production.
