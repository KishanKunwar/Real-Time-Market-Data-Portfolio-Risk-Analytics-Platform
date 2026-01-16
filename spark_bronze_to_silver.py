from pyspark.sql import SparkSession
from pyspark.sql.functions import upper, trim, to_date

spark = (
    SparkSession.builder
    .appName("Bronze To Silver")
    .config("spark.sql.shuffle.partitions", "1")
    .getOrCreate()
)

# Read Bronze (batch)
bronze_df = spark.read.parquet("./Data/Bronze/finance")

# Transform to Silver
silver_df = (
    bronze_df
    .withColumn("symbol", upper(trim("symbol")))
    .withColumn("trade_date", to_date("date"))
    .dropDuplicates(["symbol", "date"])
)

# Write Silver (batch)
(
    silver_df
    .write
    .mode("overwrite")   
    .partitionBy("trade_date")
    .parquet("./Data/Silver/finance")
)
