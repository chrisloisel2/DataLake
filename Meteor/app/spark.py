from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

# Initialize Spark session
spark = SparkSession.builder \
	.appName("KafkaSparkStreaming") \
	.getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Define Kafka parameters
kafka_bootstrap_servers = "kafka:9092"
kafka_topic = "topic1"

# Read data from Kafka
df = spark \
	.readStream \
	.format("kafka") \
	.option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
	.option("subscribe", kafka_topic) \
	.load()


schema = StructType([
    StructField("id", StringType(), True),
	StructField("nom", StringType(), True),
	StructField("prenom", StringType(), True),
	StructField("age", StringType(), True),
	StructField("email", StringType(), True),
	StructField("preferences", StringType(), True),
	StructField("solde", StringType(), True),
	StructField("ne", StringType(), True)
])


parsed_df = df.selectExpr("CAST(value AS STRING)") \
	.select(from_json(col("value"), schema).alias("data")) \
	.select("data.*")

# Write the parsed data to the console
query = parsed_df.writeStream \
	.outputMode("append") \
	.format("console") \
	.start()

query.awaitTermination()
