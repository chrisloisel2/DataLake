from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, avg, explode, window, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, ArrayType

# Configuration de la session Spark
spark = SparkSession.builder \
	.appName("KafkaSparkConsumer") \
	.config("spark.sql.catalogImplementation", "hive") \
	.config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1)") \
    .enableHiveSupport() \
	.getOrCreate()

# Schema des donnees kafka

# mute les messages d'erreur
spark.sparkContext.setLogLevel("ERROR")

# {
#   "sensor_id": "sensor_12345",
#   "timestamp": "2024-04-07T12:00:00Z",
#   "temperature": 22.5,
#   "humidity": 45.2
# }

sensor_schema = StructType([
    StructField("sensor_id", StringType(), True),
	StructField("timestamp", StringType(), True),
	StructField("temperature", FloatType(), True),
	StructField("humidity", FloatType(), True)
])


# consomer ma pipeline kafka via topic1

df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "topic1") \
    .option("startingOffsets", "earliest") \
    .load()


# Convertir les donnees kafka en json

df_kafka = df_kafka.selectExpr("CAST(value AS STRING)") \


# Appliquer le schema sur les donnees json

df_kafka = df_kafka.select(from_json(col("value"), sensor_schema).alias("data")) \
    .select("data.*")

# afficher les donnees kafka

df_kafka.printSchema()

# Ecrire les donnees dans la console

# query = df_kafka.writeStream \
#     .outputMode("append") \
# 	.format("console") \
# 	.start()


spark.sql("SHOW DATABASES").show()

spark.sql("CREATE DATABASE IF NOT EXISTS sensor")


spark.sql("USE sensor")

spark.sql("DROP TABLE IF EXISTS sensor_data")

spark.sql("""
	CREATE TABLE IF NOT EXISTS sensor_data (
		sensor_id STRING,
		timestamp STRING,
		temperature FLOAT,
		humidity FLOAT
	) USING hive
""")


# Ecrire les donnees dans la table hive

query = df_kafka.writeStream \
	.outputMode("append") \
	.format("hive") \
	.option("checkpointLocation", "/tmp/sensor_data_checkpoint") \
	.start("sensor.sensor_data")

query.awaitTermination()
