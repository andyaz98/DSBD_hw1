from confluent_kafka import Consumer, Producer
import json
from datetime import datetime
import cqrs_alert_system
from produce_sync import produce_sync
import time

time.sleep(30)


# Kafka configuration for consumer and producer
consumer_config = {
    'bootstrap.servers': 'broker_1:9092,broker_2:9092,broker_3:9092',  # Kafka broker address
    'group.id': 'group1',  # Consumer group ID
    'auto.offset.reset': 'earliest',  # Start reading from the earliest message
    'enable.auto.commit': False
}

producer_config = {
    # NB: se il producer viene inserito in un container va messo come indirizzo -> '<container_name>:<porta definita in PLAINTEXT>' es. 'kafka:9092'
    'bootstrap.servers': 'broker_1:9092,broker_2:9092,broker_3:9092',  # Kafka broker address
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
                consumer.commit(asynchronous=True)


if __name__ == "__main__":
    alert_system()
