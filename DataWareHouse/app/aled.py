from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HiveIntegration") \
    .config("spark.sql.catalogImplementation", "hive") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("SHOW DATABASES").show()

spark.sql("CREATE DATABASE IF NOT EXISTS my_database")
spark.sql("USE my_database")

spark.sql("SHOW DATABASES").show()

spark.sql("DROP TABLE IF EXISTS user")

spark.sql("""
    CREATE TABLE IF NOT EXISTS user (
        id INT,
        name STRING,
        age INT
    )
""")

data = [
    (1, 'John', 25),
    (2, 'Jane', 30),
    (3, 'Alice', 35)
]

df = spark.createDataFrame(data, ['id', 'name', 'age'])
df.write.mode('overwrite').saveAsTable('user')

spark.sql("SHOW TABLES").show()

df_hive = spark.sql("SELECT * FROM user")
df_hive.show()
