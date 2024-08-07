from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, avg, explode, window, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, ArrayType

# Configuration de la session Spark
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .config("spark.master", "local[*]") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

# Schéma des données utilisateur
user_schema = StructType([
    StructField("id", StringType(), True),
    StructField("nom", StringType(), True),
    StructField("prenom", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("email", StringType(), True),
    StructField("preferences", ArrayType(StringType()), True),
    StructField("solde", FloatType(), True),
    StructField("ne", IntegerType(), True)
])

# Consommation des messages Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "topic1") \
    .load()

# Déserialiser les messages Kafka
user_df = df.selectExpr("CAST(value AS STRING)", "timestamp") \
    .select(from_json(col("value"), user_schema).alias("data"), col("timestamp")) \
    .select("data.*", "timestamp")

# Ajouter un watermark pour gérer les données tardives
user_df_with_watermark = user_df.withWatermark("timestamp", "10 minutes")

# Calcul de la moyenne d'âge des utilisateurs avec watermark
avg_age = user_df_with_watermark.groupBy(window(col("timestamp"), "10 minutes")).agg(avg(col("age")).alias("average_age"))

# Distribution des préférences avec watermark
preferences_exploded = user_df_with_watermark.select(explode(col("preferences")).alias("preference"), "timestamp")
preference_distribution = preferences_exploded.groupBy(window(col("timestamp"), "10 minutes"), "preference").count()

# Écrire les résultats dans HDFS en Parquet
query_avg_age = avg_age.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/user/spark/average_age") \
    .option("checkpointLocation", "/user/spark/average_age_checkpoint") \
    .start()

query_preference_distribution = preference_distribution.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/user/spark/preference_distribution") \
    .option("checkpointLocation", "/user/spark/preference_distribution_checkpoint") \
    .start()

# Attendre la fin des requêtes
query_avg_age.awaitTermination()
query_preference_distribution.awaitTermination()
