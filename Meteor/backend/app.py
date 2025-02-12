from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from confluent_kafka import Producer
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

KAFKA_BROKER = "kafka:9092"
TOPIC_NAME = "topic1"

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

db.create_all()

@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([{"id": item.id, "name": item.name, "description": item.description} for item in items])

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify({"id": item.id, "name": item.name, "description": item.description})

@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    new_item = Item(name=data["name"], description=data.get("description"))
    db.session.add(new_item)
    db.session.commit()

    event_data = f'{new_item.id},{new_item.name},{new_item.description}'
    producer.produce(TOPIC_NAME, key=str(new_item.id), value=event_data)
    producer.flush()

    return jsonify({"message": "Item created", "id": new_item.id}), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.json
    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)
    db.session.commit()
    return jsonify({"message": "Item updated"})

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5550)
