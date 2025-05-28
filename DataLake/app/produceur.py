from kafka import KafkaProducer
import json

# Configuration
KAFKA_BROKER = 'kafka:9092'
TOPIC = 'topic1'

# Create Kafka producer
producer = KafkaProducer(
	bootstrap_servers=KAFKA_BROKER,
	value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_message(message):
	producer.send(TOPIC, message)
	producer.flush()

if __name__ == "__main__":
	# Example usage
	msg = {"key": "value"}
	send_message(msg)
	print("Message sent to topic:", TOPIC, "with content:", msg)
