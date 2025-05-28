from pyspark.sql import SparkSession


# Create a SparkSession
spark = SparkSession.builder \
	.appName("Read from HDFS") \
	.getOrCreate()

# SParkContext
sc = spark.sparkContext

# Read the file from HDFS
df = spark.read.text("hdfs://namenode:9000/data.csv")

# Creation de mon RDD
rdd = sc.textFile("hdfs://namenode:9000/data.csv")

# Print toute les lignes

# all_lines = rdd.collect()
# for line in all_lines:
# 	print(line)


# Count
# line_count = rdd.count()
# print("Total number of lines:", line_count)

# Print the schema of the DataFrame
# df.printSchema()

# Take(N) to get the first N lines
# first_lines = df.take(5)
# for line in first_lines:
# 	print(line)

# Show the first few rows of the DataFrame
# df.show(5)

# First()
# first_row = df.first()
# print("First row:", first_row)

# TOP(N) to get the first N rows
# top_rows = df.head(5)
# for row in top_rows:
# 	print(row)

# MAP

# mapped_rdd = rdd.map(lambda x: x.split(","))
# print("Mapped RDD:", mapped_rdd.collect())

# FILTER

def filter_function(line):
    return "Emma" in line

filtered_rdd = rdd.filter(filter_function)
print("Filtered RDD:", filtered_rdd.collect())

# # Reduce by key (example)

reduced_rdd = rdd.map(lambda x: (x.split(",")[0], x.split(",")[1])).reduceByKey(lambda a, b: a + b)
print("Reduced RDD:", reduced_rdd.collect())

# Add, sum, substract, multiply, divide (example)

# Example of arithmetic operations
arrithmetic_rdd = rdd.map(lambda x: int(x.split(",")[1]) * 2)  # Assuming the second column is numeric
print("Arithmetic RDD:", arrithmetic_rdd.collect())

arrithmetic_rdd_sum = arrithmetic_rdd.reduce(lambda a, b: a + b)
print("Sum of arithmetic RDD:", arrithmetic_rdd_sum)


# Show the contents of the file
# df.show()

# Close the SparkSession
spark.stop()
