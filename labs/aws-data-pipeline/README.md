# AWS Data Engineering Lab

Hands-on lab focused on a small serverless analytics pipeline using AWS services commonly used in data engineering workloads.

## Goal

Build a simple pipeline that:

1. Uploads raw CSV data to Amazon S3 with Python/Boto3.
2. Uses AWS Glue Data Catalog and a Glue Crawler to discover the schema.
3. Transforms the raw dataset with a Glue PySpark job.
4. Writes curated Parquet data back to S3.
5. Queries the curated dataset with Amazon Athena.
6. Provisions the core infrastructure with Terraform.

## Architecture

```text
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

## Skills demonstrated

- Python
- Boto3
- AWS S3
- AWS Glue Jobs
- AWS Glue Crawlers
- PySpark
- Amazon Athena
- SQL
- Terraform
- IAM
- Git

## Repository structure

```text
labs/aws-data-pipeline/
├── README.md
├── python/
│   └── upload_to_s3.py
├── glue/
│   └── transform_sales.py
├── sql/
│   └── analytics.sql
├── terraform/
│   └── main.tf
└── requirements.txt
```

## Example dataset

The pipeline expects a CSV with the following columns:

```text
order_id,customer_id,product,quantity,unit_price,order_date
1001,C001,Keyboard,1,45.90,2026-08-01
1002,C002,Mouse,2,19.90,2026-08-01
```

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure AWS credentials using the AWS CLI or environment variables, then upload a dataset:

```bash
python python/upload_to_s3.py --bucket YOUR_BUCKET --file sales.csv
```

## Notes

This project is intentionally small enough to explain end-to-end in an interview. The focus is on understanding the data flow, IAM permissions, schema discovery, transformation, partition-friendly Parquet output and SQL analytics rather than on building a production-scale platform.
