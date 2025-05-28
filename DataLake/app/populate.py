from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType


spark = SparkSession.builder \
    .appName("Populate Data WareHouse hive") \
    .config("spark.sql.catalogImplementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()


spark.sql("CREATE DATABASE IF NOT EXISTS maps")

# Define the schema for the DataFrame
schema = StructType([
	StructField("nom", StringType(), True),
	StructField("prenom", StringType(), True),
	StructField("age", IntegerType(), True),
	StructField("ca", DoubleType(), True),
])

data = [
	("Dupont", "Jean", 28, 1000.0),
	("Dupont", "Marie", 32, 1500.0),
	("Durand", "Pierre", 45, 2000.0),
	("Martin", "Lucie", 29, 2500.0),
	("Bernard", "Paul", 35, 3000.0),
	("Bernard", "Sophie", 40, 3500.0),
	("Lemoine", "Alice", 27, 1200.0),
	("Morel", "Julien", 33, 1800.0),
	("Roux", "Claire", 38, 2200.0),
	("Fournier", "Hugo", 41, 2700.0),
	("Girard", "Emma", 30, 3200.0),
	("Blanc", "Lucas", 36, 3700.0),
	("Fontaine", "Chloe", 25, 1100.0),
	("Chevalier", "Nathan", 34, 1900.0),
	("Robin", "Camille", 39, 2300.0),
	("Gauthier", "Leo", 42, 2800.0),
	("Perrin", "Manon", 31, 3300.0),
	("Morin", "Louis", 37, 3800.0),
	("Noel", "Sarah", 26, 1150.0),
	("Bertrand", "Theo", 35, 1950.0),
	("Vidal", "Laura", 40, 2400.0),
	("Moulin", "Maxime", 43, 2900.0),
	("Dupuis", "Elise", 29, 3400.0),
	("Fabre", "Antoine", 38, 3900.0),
	("Olivier", "Julie", 28, 1250.0),
	("Regnier", "Bastien", 32, 1750.0),
	("Marchand", "Celine", 44, 2250.0),
	("Aubert", "Victor", 41, 2750.0),
	("Lemoine", "Alice", 27, 3250.0),
	("Morel", "Julien", 33, 3750.0),
	("Roux", "Claire", 38, 1200.0),
	("Fournier", "Hugo", 41, 1700.0),
	("Girard", "Emma", 30, 2200.0),
	("Blanc", "Lucas", 36, 2700.0),
	("Fontaine", "Chloe", 25, 3200.0),
	("Chevalier", "Nathan", 34, 3700.0),
	("Robin", "Camille", 39, 1100.0),
	("Gauthier", "Leo", 42, 1600.0),
	("Perrin", "Manon", 31, 2100.0),
	("Morin", "Louis", 37, 2600.0),
	("Noel", "Sarah", 26, 3100.0),
	("Bertrand", "Theo", 35, 3600.0),
	("Vidal", "Laura", 40, 1150.0),
	("Moulin", "Maxime", 43, 1650.0),
	("Dupuis", "Elise", 29, 2150.0),
	("Fabre", "Antoine", 38, 2650.0),
	("Olivier", "Julie", 28, 3150.0),
	("Regnier", "Bastien", 32, 3650.0),
	("Marchand", "Celine", 44, 1200.0),
	("Aubert", "Victor", 41, 1700.0),
	("Lemoine", "Alice", 27, 2200.0),
	("Morel", "Julien", 33, 2700.0),
	("Roux", "Claire", 38, 3200.0),
	("Fournier", "Hugo", 41, 3700.0),
	("Girard", "Emma", 30, 1100.0),
	("Blanc", "Lucas", 36, 1600.0),
	("Fontaine", "Chloe", 25, 2100.0),
	("Chevalier", "Nathan", 34, 2600.0),
	("Robin", "Camille", 39, 3100.0),
	("Gauthier", "Leo", 42, 3600.0)
]



df = spark.createDataFrame(data, schema)
df.write.mode("overwrite").saveAsTable("maps.maps")
