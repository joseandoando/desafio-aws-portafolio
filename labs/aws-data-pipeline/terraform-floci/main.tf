terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "endpoint" {
  type    = string
  default = "http://localhost:4566"
}

variable "bucket_name" {
  type    = string
  default = "jose-data-engineering-lab-local"
}

variable "database_name" {
  type    = string
  default = "jose_data_engineering_lab_db"
}

provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3     = var.endpoint
    glue   = var.endpoint
    athena = var.endpoint
    sts    = var.endpoint
  }
}

resource "aws_s3_bucket" "data" {
  bucket        = var.bucket_name
  force_destroy = true
}

resource "aws_glue_catalog_database" "analytics" {
  name = var.database_name
}

resource "aws_glue_catalog_table" "raw_sales" {
  name          = "raw_sales"
  database_name = aws_glue_catalog_database.analytics.name
  table_type    = "EXTERNAL_TABLE"

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.data.bucket}/raw/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.serde2.OpenCSVSerde"
    }

    columns { name = "order_id" type = "int" }
    columns { name = "customer_id" type = "string" }
    columns { name = "product" type = "string" }
    columns { name = "quantity" type = "int" }
    columns { name = "unit_price" type = "double" }
    columns { name = "order_date" type = "string" }
  }
}

resource "aws_glue_catalog_table" "curated_sales" {
  name          = "curated_sales"
  database_name = aws_glue_catalog_database.analytics.name
  table_type    = "EXTERNAL_TABLE"

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.data.bucket}/curated/sales/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }

    columns { name = "order_id" type = "int" }
    columns { name = "customer_id" type = "string" }
    columns { name = "product" type = "string" }
    columns { name = "quantity" type = "int" }
    columns { name = "unit_price" type = "double" }
    columns { name = "order_date" type = "date" }
    columns { name = "total_amount" type = "double" }
    columns { name = "year" type = "int" }
    columns { name = "month" type = "int" }
  }
}

resource "aws_athena_workgroup" "analytics" {
  name = "jose-data-engineering-local"

  configuration {
    enforce_workgroup_configuration = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.data.bucket}/athena-results/"
    }
  }
}

output "bucket_name" {
  value = aws_s3_bucket.data.bucket
}

output "glue_database" {
  value = aws_glue_catalog_database.analytics.name
}
