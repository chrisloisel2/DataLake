from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HiveIntegration") \
    .config("spark.sql.catalogImplementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("SHOW DATABASES").show()

# Create database
spark.sql("CREATE DATABASE IF NOT EXISTS my_database")
spark.sql("USE my_database")

# Create user table
spark.sql("""
	CREATE TABLE IF NOT EXISTS user (
		id INT,
		name STRING,
		age INT
	)
""")

# Populate the database
data = [
	(1, 'John', 25),
	(2, 'Jane', 30),
	(3, 'Alice', 35)
]

df = spark.createDataFrame(data, ['id', 'name', 'age'])
df.write.mode('overwrite').saveAsTable('user')
