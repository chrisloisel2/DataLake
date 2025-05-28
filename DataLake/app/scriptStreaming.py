from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Creer la session Spark
spark = SparkSession.builder.appName("StocksToHDFS").getOrCreate()

# Mute les logs inferieur au niveau Warning
spark.sparkContext.setLogLevel("WARN")

# Selectionner mon topic
kafka_topic_name = "topic1"

# Selectionner mon server
kafka_bootstrap_servers = 'kafka:9092'

# Recuperation de mes data de mon stream kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
  .option("subscribe", kafka_topic_name) \
  .load()

# Caster les data de mon string pour les rendre utilisables
df = df.selectExpr("CAST(value AS STRING)")


query = df \
    .writeStream.outputMode("append") \
    .format("console") \
    .start()

# Sauvegarder les data dans un fichier

# query = df \
#     .writeStream \
# 	.format("text") \
# 	.outputMode("append") \
# 	.option("path", "hdfs://namenode:9000/Data/stocks") \
# 	.option("checkpointLocation", "hdfs://namenode:9000/Data/stocks/checkpoint") \
# 	.start()


# Ne pas terminer le fichier tant que mon stream n'est pas finit
query.awaitTermination()
