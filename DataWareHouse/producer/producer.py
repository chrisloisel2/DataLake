from kafka import KafkaProducer
from time import sleep
import json
import random
from datetime import datetime

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_data():
    return {
        'sensor_id': random.randint(1, 100),
        'temperature': random.uniform(20.0, 30.0),
        'humidity': random.uniform(30.0, 60.0),
        'timestamp': datetime.utcnow().isoformat()
    }

while True:
    data = generate_data()
    producer.send('topic1', data)
    print(f"Sent data: {data}")
    sleep(2)
