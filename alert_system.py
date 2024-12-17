from confluent_kafka import Consumer, Producer
import json
from datetime import datetime
import cqrs_alert_system

# ESEMPIO IN CUI IL CONUSUMER HA AUTO COMMIT ABILITATO E INOLTRE E' ANCHE PRODUCER

# Kafka configuration for consumer and producer
consumer_config = {
    'bootstrap.servers': 'localhost:19092,localhost:29092,localhost:39092',  # Kafka broker address
    'group.id': 'group1',  # Consumer group ID
    'auto.offset.reset': 'earliest',  # Start reading from the earliest message
    'enable.auto.commit': True,  # Automatically commit offsets periodically
    'auto.commit.interval.ms': 5000  # Commit offsets every 5000ms (5 seconds)
}

producer_config = {
    # NB: se il producer viene inserito in un container va messo come indirizzo -> '<container_name>:<porta definita in PLAINTEXT>' es. 'kafka:9092'
    'bootstrap.servers': 'localhost:19092,localhost:29092,localhost:39092',  # Kafka broker address
    'acks': 'all',  # Ensure all in-sync replicas acknowledge the message
    'batch.size': 500,  # Maximum number of bytes to batch in a single request
    'max.in.flight.requests.per.connection': 1,  # Only one in-flight request per connection
    'retries': 3  # Retry up to 3 times on failure
}

consumer = Consumer(consumer_config)
producer = Producer(producer_config)

alert_system_topic = "to-alert-system"  # Source topic for input messages
notifier_topic = 'to-notifier'  # Destination topic for output statistics

consumer.subscribe([alert_system_topic])  # Subscribe to TOPIC1

def alert_system():
    find_users_to_notify_service = cqrs_alert_system.FindUsersToNotifyService()

    while True:
        # Poll for new messages from TOPIC1
        msg = consumer.poll(1.0)
        if msg is None:
            continue  # No message received, continue polling
        if msg.error():
            print(f"Consumer error: {msg.error()}")  # Log any consumer errors
            continue
        
        # Parse the received message
        data = json.loads(msg.value().decode('utf-8'))

        if data["updated_tickers"]:
            print(f"Message arrived with timestamp: {data["timestamp"]}")
            rows = find_users_to_notify_service.handle_get_users()

            for row in rows:
                email, ticker, condition = row

                message = {
                'timestamp': datetime.now().isoformat(),
                'email': email,
                'ticker': ticker,
                'condition': condition
                }

                produce_sync(producer, notifier_topic, json.dumps(message))

def produce_sync(producer, topic, value):
    """
    Synchronous producer function that blocks until the message is sent.
    :param producer: Kafka producer instance
    :param topic: Kafka topic to send the message to
    :param value: Message value (string)
    """
    try:
        # Produce the message synchronously
        producer.produce(topic, value)
        producer.flush()  # Block until all outstanding messages are sent
        print(f"Synchronously produced message to {topic}: {value}")
    except Exception as e:
        print(f"Failed to produce message: {e}") 

if __name__ == "__main__":
    alert_system()
