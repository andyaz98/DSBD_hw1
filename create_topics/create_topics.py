from confluent_kafka.admin import AdminClient, NewTopic
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

bootstrap_servers = "broker-1:9092"

# Definizione di un semplice handler per il server HTTP
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Service is up!")

# Funzione per avviare il server HTTP
def start_http_server():
    server = HTTPServer(('0.0.0.0', 2222), SimpleHandler)
    print("HTTP server running on port 2222...")
    server.serve_forever()

# Ritardo iniziale
time.sleep(20)

# Creazione dei topic
while True:
    try:
        admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

        new_topic = [NewTopic('to-notifier', num_partitions=1, replication_factor=3),
                     NewTopic('to-alert-system', num_partitions=1, replication_factor=3)]
        
        # Creazione dei topic
        fs = admin_client.create_topics(new_topics=new_topic)
        
        for topic, f in fs.items():
            try:
                f.result()  # Il risultato è None se l'operazione ha successo
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

# Avvio il server HTTP in modo tale da poter verificare che il servizio sia attivo
start_http_server()