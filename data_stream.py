import logging
import json
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf


schema = StructType(
    [
        StructField("crime_id", StringType(), False),
        StructField("original_crime_type_name", StringType()),
        StructField("report_date", StringType()),
        StructField("call_date", StringType()),
        StructField("offense_date", StringType()),
        StructField("call_time", StringType()),
        StructField("call_date_time", StringType()),
        StructField("disposition", StringType()),
        StructField("disposition_date", StringType()),
        StructField("address", StringType()),
        StructField("city", StringType()),
        StructField("state", StringType()),
        StructField("agency_id", StringType()),
        StructField("address_type", StringType()),
        StructField("common_location", StringType()),
    ]
)


def run_spark_job(spark):
    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "udacity_projects.sf_crime_rate.pd_calls_for_service")
        .option("startingOffsets", "earliest")
        .option("maxOffsetsPerTrigger", 200)
        .load()
    )

    # Show schema for the incoming resources for checks
    df.printSchema()

    kafka_df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    service_table = kafka_df.select(
        psf.col("key").cast("string"),
        psf.from_json(psf.col("value"), schema).alias("value"),
    ).select("value.*")
    service_table.printSchema()

    distinct_table = service_table.select(
        psf.col("original_crime_type_name"),
        psf.col("disposition"),
        psf.col("call_date_time"),
    )
    distinct_table.printSchema()

    # count the number of original crime type
    agg_df = (
        distinct_table.withColumn(
            "call_date_seconds", psf.col("call_date_time").astype("Timestamp")
        )
        .withWatermark("call_date_seconds", "10 minutes")
        .groupBy(
            psf.window(psf.col("call_date_seconds"), "30 minutes"),
            psf.col("original_crime_type_name"),
            psf.col("disposition"),
        )
        .agg(psf.count(psf.col("original_crime_type_name")).alias("count"))
        .orderBy(psf.col("window"))
    )

    agg_df.printSchema()

    radio_code_json_filepath = os.getcwd() + "/data/radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath, multiLine=True)
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")

    radio_code_df.printSchema()

    join_query = (
        agg_df.join(radio_code_df, agg_df.disposition == radio_code_df.disposition)
        .select("window", "original_crime_type_name", "description", "count")
        .writeStream.format("console")
        .outputMode("complete")
        .option("truncate", "false")
        .start()
    )

    join_query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # Create Spark in Standalone mode
    spark = (
        SparkSession.builder.master("local[*]")
        .appName("KafkaSparkStructuredStreaming")
        .getOrCreate()
    )

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()
