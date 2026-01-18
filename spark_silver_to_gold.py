from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, min, sum, year, month, dayofmonth, quarter, dayofweek
import psycopg2

# ======================
# Initialize Spark
# ======================
spark = (
    SparkSession.builder
    .appName("Silver To Gold - Kimball")
    .config("spark.jars", "/Users/kishankunwar/Downloads/postgresql-42.7.8.jar")
    .getOrCreate()
)

# ======================
# Read SILVER
# ======================
silver_df = spark.read.parquet("./Data/Silver/finance")

# ======================
# DIMENSION: SYMBOL
# ======================
dim_symbol = silver_df.select("symbol").dropDuplicates()

# ======================
# DIMENSION: DATE
# ======================
dim_date = (
    silver_df
    .select("trade_date")
    .dropDuplicates()
    .withColumn("year", year("trade_date"))
    .withColumn("month", month("trade_date"))
    .withColumn("day", dayofmonth("trade_date"))
    .withColumn("quarter", quarter("trade_date"))
    .withColumn("weekday", dayofweek("trade_date"))
)

# ======================
# FACT TABLE
# ======================
fact_finance = (
    silver_df
    .groupBy("symbol", "trade_date")
    .agg(
        avg("close").alias("avg_close"),
        max("high").alias("max_high"),
        min("high").alias("min_high"),
        avg("low").alias("avg_low"),
        sum("volume").alias("total_volume")
    )
)

# ======================
# JDBC CONFIG
# ======================
jdbc_url = "jdbc:postgresql://localhost:5432/finance_gold"
postgres_props = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

# ======================
# Helper function: TRUNCATE + append
# ======================
def safe_truncate_and_write(df, table_name):
    # 1. Truncate table in Postgres
    conn = psycopg2.connect(
        dbname="finance_gold",
        user="postgres",
        password="postgres",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute(f"TRUNCATE TABLE {table_name};")
    conn.commit()
    cur.close()
    conn.close()

    # 2. Append Spark DataFrame
    df.write.mode("append").jdbc(url=jdbc_url, table=table_name, properties=postgres_props)

# ======================
# Write DIMENSIONS & FACTS
# ======================
safe_truncate_and_write(dim_symbol, "dim_symbol")
safe_truncate_and_write(dim_date, "dim_date")
safe_truncate_and_write(fact_finance, "fact_finance")

print("Data successfully loaded to GOLD tables!")
