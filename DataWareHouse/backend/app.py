from flask import Flask, request, jsonify
from kafka import KafkaProducer
from marshmallow import Schema, fields, ValidationError
import json

app = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class UserSchema(Schema):
    id = fields.Str(required=True)
    nom = fields.Str(required=True)
    prenom = fields.Str(required=True)
    age = fields.Int(required=True)
    email = fields.Email(required=True)
    preferences = fields.List(fields.Str(), required=True)
    solde = fields.Float(required=True)
    ne = fields.Int(required=True)

user_schema = UserSchema()

@app.route('/user', methods=['POST'])
def add_user():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    producer.send('topic1', data)
    producer.flush()

    return jsonify({"message": "User data received and sent to Kafka"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5550)
