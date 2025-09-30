import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from pyspark.sql.functions import col, when, year, to_date

RAW_DATA_FILE = os.path.join("data", "raw", "airbnb.csv")
PROCESSED_DATA_DIR = os.path.join("data", "processed")

def transform_airbnb_data():
    spark = SparkSession.builder.appName("AirbnbTransform").getOrCreate()

    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("host_id", IntegerType(), True),
        StructField("host_name", StringType(), True),
        StructField("neighbourhood_group", StringType(), True),
        StructField("neighbourhood", StringType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("room_type", StringType(), True),
        StructField("price", IntegerType(), True),
        StructField("minimum_nights", IntegerType(), True),
        StructField("number_of_reviews", IntegerType(), True),
        StructField("last_review", StringType(), True),
        StructField("reviews_per_month", DoubleType(), True),
        StructField("calculated_host_listings_count", IntegerType(), True),
        StructField("availability_365", IntegerType(), True)
    ])

    print(f"[INFO] Reading data from {RAW_DATA_FILE}")
    df = spark.read.csv(RAW_DATA_FILE, header=True, schema=schema)

    df = df.withColumn("last_review_clean", when(col("last_review").rlike(r"^\d{4}-\d{2}-\d{2}$"), col("last_review")))
    df = df.withColumn("last_review", to_date(col("last_review_clean"), "yyyy-MM-dd")).drop("last_review_clean")

    invalid_count = df.filter(col("last_review").isNull()).count()
    print(f"[WARN] Invalid or missing last_review rows: {invalid_count}")

    df = df.filter(col("price") > 0)
    df = df.filter(col("price") < 10000)
    df = df.filter((col("minimum_nights") > 0) & (col("minimum_nights") < 365))
    df = df.fillna({"reviews_per_month": 0})

    df = df.withColumn("year", year("last_review"))
    df = df.withColumn("price_bucket", when(col("price") < 100, "Low").when((col("price") >= 100) & (col("price") <= 300), "Medium").otherwise("High"))
    df = df.withColumn("availability_flag", when(col("availability_365") > 200, "High").otherwise("Low"))
    df = df.withColumn("review_flag", when(col("number_of_reviews") == 0, "No Reviews").otherwise("Has Reviews"))

    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    output_path = os.path.join(PROCESSED_DATA_DIR, "airbnb_cleaned_csv")

    print(f"[INFO] Saving transformed data to {output_path}")
    df.write.mode("overwrite").parquet(output_path)

    spark.stop()
    print("[INFO] Transform step completed.")
    return output_path

if __name__ == "__main__":
    transform_airbnb_data()
