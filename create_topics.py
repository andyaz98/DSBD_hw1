from confluent_kafka.admin import AdminClient, NewTopic
import time

time.sleep(20)

bootstrap_servers = "broker_1:9092"  

while True:
    try:
        admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

        new_topic = [NewTopic('to-notifier', num_partitions=1, replication_factor=3), 
                    NewTopic('to-alert-system', num_partitions=1, replication_factor=3)]
        
        # Create topics
        fs = admin_client.create_topics(new_topics=new_topic)
        
        # Wait for each operation to finish
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print(f"Topic {topic} created successfully")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
        break
    except Exception as e:
        print(f"An exception occurred - {e}")

def list_kafka_topics(bootstrap_servers):
    # Creazione di un client amministrativo
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

    try:
        # Ottieni i metadati del cluster
        metadata = admin_client.list_topics(timeout=10)
        
        # Estrai e stampa la lista dei topic
        topics = metadata.topics
        print("Lista dei topic:")
        for topic in topics:
            print(f"- {topic}")
    except Exception as e:
        print(f"Errore durante il recupero dei topic: {e}")

# Specifica l'indirizzo del broker Kafka

list_kafka_topics(bootstrap_servers)
