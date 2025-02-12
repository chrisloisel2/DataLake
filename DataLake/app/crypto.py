from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max

spark = SparkSession.builder \
	.appName("Read from HDFS") \
	.getOrCreate()


# mute le niveau de log
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("hdfs://namenode:9000/Data/crypto_data_part_1(2).csv", header=True, inferSchema=True)

avg_closing_price = df.groupBy("Cryptomonnaie").agg(avg("PrixCloture").alias("PrixClotureMoyen"))

max_vomule = df.groupBy("Date").agg(max("Volume").alias("VolumeMax"))

avg_closing_price.show()
max_vomule.show()


# Ajouter les colonnes au DataFrame
df = df.join(avg_closing_price, "Cryptomonnaie")
df = df.join(max_vomule, "Date")

# Sauvegarder le DataFrame
df.write.csv("hdfs://namenode:9000/Data/crypto_data_part_1(2)_modified.csv")

spark.stop()
