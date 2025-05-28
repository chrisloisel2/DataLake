from flask import Flask, request
from kafka import KafkaProducer

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:9092')


@app.route('/', methods=['POST'])
def send_message():
	message = request.json.get('message')
	producer.send('topic1', message.encode('utf-8'))
	producer.flush()
	return 'Message sent to Kafka topic'

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
