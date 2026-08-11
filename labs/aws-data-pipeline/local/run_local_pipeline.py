import os
import shutil
import tempfile
import time
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, EndpointConnectionError
from pyspark.sql import SparkSession, functions as F


ENDPOINT = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
BUCKET = os.getenv("LAB_BUCKET", "jose-data-engineering-lab-local")
DATABASE = os.getenv("GLUE_DATABASE", "jose_data_engineering_lab_db")
RAW_TABLE = "raw_sales"
CURATED_TABLE = "curated_sales"

SESSION = boto3.session.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    region_name=REGION,
)


def client(service: str):
    kwargs = {"endpoint_url": ENDPOINT}
    if service == "s3":
        kwargs["config"] = Config(s3={"addressing_style": "path"})
    return SESSION.client(service, **kwargs)


s3 = client("s3")
glue = client("glue")
athena = client("athena")
sts = client("sts")


def wait_for_floci(timeout: int = 60) -> None:
    print(f"[1/7] Waiting for Floci at {ENDPOINT} ...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            identity = sts.get_caller_identity()
            print(f"      Floci ready. Account: {identity.get('Account', 'local')}")
            return
        except (ClientError, EndpointConnectionError):
            time.sleep(1)
    raise TimeoutError("Floci did not become ready before timeout")


def ensure_bucket() -> None:
    print(f"[2/7] Preparing S3 bucket: {BUCKET}")
    try:
        s3.head_bucket(Bucket=BUCKET)
    except ClientError:
        s3.create_bucket(Bucket=BUCKET)


def upload_raw_dataset() -> Path:
    source = Path("sample/sales.csv")
    if not source.exists():
        raise FileNotFoundError(f"Dataset not found: {source}")

    print("[3/7] Uploading raw CSV with Boto3")
    s3.upload_file(str(source), BUCKET, "raw/sales.csv")
    print(f"      s3://{BUCKET}/raw/sales.csv")
    return source


def run_pyspark_transform(source: Path) -> None:
    print("[4/7] Running local PySpark transformation")
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("aws-data-engineering-floci-lab")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    raw = spark.read.option("header", True).option("inferSchema", True).csv(str(source))
    clean = (
        raw.dropna(subset=["order_id", "customer_id", "order_date"])
        .withColumn("quantity", F.col("quantity").cast("int"))
        .withColumn("unit_price", F.col("unit_price").cast("double"))
        .withColumn("order_date", F.to_date("order_date"))
        .withColumn("total_amount", F.round(F.col("quantity") * F.col("unit_price"), 2))
        .withColumn("year", F.year("order_date"))
        .withColumn("month", F.month("order_date"))
    )

    temp_dir = Path(tempfile.mkdtemp(prefix="sales-curated-"))
    parquet_dir = temp_dir / "sales"
    clean.coalesce(1).write.mode("overwrite").parquet(str(parquet_dir))

    for parquet_file in parquet_dir.glob("part-*.parquet"):
        key = f"curated/sales/{parquet_file.name}"
        s3.upload_file(str(parquet_file), BUCKET, key)
        print(f"      uploaded s3://{BUCKET}/{key}")

    spark.stop()
    shutil.rmtree(temp_dir, ignore_errors=True)


def ensure_database() -> None:
    try:
        glue.get_database(Name=DATABASE)
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") not in {"EntityNotFoundException", "404"}:
            raise
        glue.create_database(DatabaseInput={"Name": DATABASE})


def ensure_table(name: str, table_input: dict) -> None:
    try:
        glue.get_table(DatabaseName=DATABASE, Name=name)
        return
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") not in {"EntityNotFoundException", "404"}:
            raise
    glue.create_table(DatabaseName=DATABASE, TableInput=table_input)


def register_catalog() -> None:
    print("[5/7] Registering Glue Data Catalog metadata")
    ensure_database()

    ensure_table(
        RAW_TABLE,
        {
            "Name": RAW_TABLE,
            "TableType": "EXTERNAL_TABLE",
            "StorageDescriptor": {
                "Location": f"s3://{BUCKET}/raw/",
                "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                "SerdeInfo": {
                    "SerializationLibrary": "org.apache.hadoop.hive.serde2.OpenCSVSerde"
                },
                "Columns": [
                    {"Name": "order_id", "Type": "int"},
                    {"Name": "customer_id", "Type": "string"},
                    {"Name": "product", "Type": "string"},
                    {"Name": "quantity", "Type": "int"},
                    {"Name": "unit_price", "Type": "double"},
                    {"Name": "order_date", "Type": "string"},
                ],
            },
        },
    )

    ensure_table(
        CURATED_TABLE,
        {
            "Name": CURATED_TABLE,
            "TableType": "EXTERNAL_TABLE",
            "StorageDescriptor": {
                "Location": f"s3://{BUCKET}/curated/sales/",
                "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
                "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
                "SerdeInfo": {
                    "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
                },
                "Columns": [
                    {"Name": "order_id", "Type": "int"},
                    {"Name": "customer_id", "Type": "string"},
                    {"Name": "product", "Type": "string"},
                    {"Name": "quantity", "Type": "int"},
                    {"Name": "unit_price", "Type": "double"},
                    {"Name": "order_date", "Type": "date"},
                    {"Name": "total_amount", "Type": "double"},
                    {"Name": "year", "Type": "int"},
                    {"Name": "month", "Type": "int"},
                ],
            },
        },
    )

    print(f"      database: {DATABASE}")
    print(f"      tables: {RAW_TABLE}, {CURATED_TABLE}")


def run_athena_query() -> None:
    print("[6/7] Running Athena SQL through Floci/DuckDB")
    query = f"""
        SELECT
            product,
            SUM(quantity) AS units_sold,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM {CURATED_TABLE}
        GROUP BY product
        ORDER BY revenue DESC
    """

    execution = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": DATABASE},
        ResultConfiguration={"OutputLocation": f"s3://{BUCKET}/athena-results/"},
    )
    query_id = execution["QueryExecutionId"]

    deadline = time.time() + 60
    while time.time() < deadline:
        status = athena.get_query_execution(QueryExecutionId=query_id)
        state = status["QueryExecution"]["Status"]["State"]
        if state == "SUCCEEDED":
            break
        if state in {"FAILED", "CANCELLED"}:
            reason = status["QueryExecution"]["Status"].get("StateChangeReason", "unknown")
            raise RuntimeError(f"Athena query {state}: {reason}")
        time.sleep(1)
    else:
        raise TimeoutError("Athena query timed out")

    result = athena.get_query_results(QueryExecutionId=query_id)
    rows = result["ResultSet"]["Rows"]
    for row in rows:
        print("      " + " | ".join(cell.get("VarCharValue", "") for cell in row["Data"]))


def show_s3_objects() -> None:
    print("[7/7] Final S3 objects")
    response = s3.list_objects_v2(Bucket=BUCKET)
    for item in response.get("Contents", []):
        print(f"      {item['Key']}")
    print("\nLocal AWS data pipeline completed successfully.")


def main() -> None:
    wait_for_floci()
    ensure_bucket()
    source = upload_raw_dataset()
    run_pyspark_transform(source)
    register_catalog()
    run_athena_query()
    show_s3_objects()


if __name__ == "__main__":
    main()
