from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
import tensorflow as tf

# Create a SparkSession
spark = SparkSession.builder \
	.appName("SparkIA") \
	.getOrCreate()

# Load the trained model


model = tf.keras.models.load_model('model.h5')
# Use the model for prediction or other tasks
# ...

# Stop the SparkSession
spark.stop()
