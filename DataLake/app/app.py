from kafka import KafkaProducer
import json



def send_message_to_kafka(topic, message, bootstrap_servers='localhost:9092'):
    """
    Envoie un message au topic Kafka spécifié.

    :param topic: Nom du topic Kafka
    :param message: Message à envoyer (dict)
    :param bootstrap_servers: Adresse du serveur Kafka
    """
    # Configurer le producteur Kafka
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    try:
        # Envoyer le message au topic
        producer.send(topic, value=message)

        # Forcer l'envoi de tous les messages en attente
        producer.flush()
        print(f"Message envoyé avec succès au topic '{topic}'")

    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")

    finally:
        # Fermer le producteur
        producer.close()

if __name__ == "__main__":
    # Nom du topic
    topic_name = 'topic1'

    # Message à envoyer
    message = {'key': 'value', 'another_key': 'another_value'}

    # Adresse du serveur Kafka
    kafka_server = 'localhost:9092'

    # Envoyer le message au topic Kafka
    send_message_to_kafka(topic_name, message, kafka_server)
