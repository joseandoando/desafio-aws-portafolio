import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F


args = getResolvedOptions(sys.argv, ["JOB_NAME", "SOURCE_PATH", "TARGET_PATH"])

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

raw = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(args["SOURCE_PATH"])
)

clean = (
    raw.dropna(subset=["order_id", "customer_id", "order_date"])
    .withColumn("quantity", F.col("quantity").cast("int"))
    .withColumn("unit_price", F.col("unit_price").cast("double"))
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("total_amount", F.round(F.col("quantity") * F.col("unit_price"), 2))
    .withColumn("year", F.year("order_date"))
    .withColumn("month", F.month("order_date"))
)

(
    clean.write.mode("overwrite")
    .partitionBy("year", "month")
    .parquet(args["TARGET_PATH"])
)

job.commit()
