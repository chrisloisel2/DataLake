from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
	.appName("Read from HDFS") \
	.getOrCreate()

# Read the file from HDFS
df = spark.read.text("hdfs://namenode:9000/liste.txt")

# Show the contents of the file
df.show()

# Close the SparkSession
spark.stop()
