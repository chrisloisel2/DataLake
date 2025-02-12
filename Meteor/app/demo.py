from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum, count, when, lit, udf
from pyspark.sql.types import IntegerType, StringType, StructType, StructField, DoubleType

# Initialize Spark session
spark = SparkSession.builder \
	.appName("DemoApp") \
    .master("local") \
	.getOrCreate()

# Schema de donnees
Schema = StructType([
    StructField("ID", IntegerType(), True),
	StructField("Name", StringType(), True),
	StructField("Age", IntegerType(), True),
	StructField("Salary", DoubleType(), True)
])


# Create a DataFrame

data = [(1, "John", 28, 1000.0),
		(2, "Alice", 30, 1200.0),
		(3, "Bob", 25, 800.0),
		(4, "Catherine", 33, 1500.0),
		(5, "David", 29, 1100.0)]

df = spark.createDataFrame(data, Schema)

df.write.csv("hdfs://namenode:9000/data.csv", header=True)

# # Load data from HDFS
# df = spark.read.csv("hdfs://namenode:9000/data.csv", header=True, schema=Schema)

# # Show the contents of the file
# df.show()


# df_select = df.select("Name", "Age", "Salary")

# df_grouped = df.groupBy("Name").agg(avg("Salary").alias("Average Salary"), sum("Salary").alias("Total Salary"), count("Salary").alias("Number of Employees"))

# df_filtered = df.filter(col("Age") > 30)
