import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from confluent_kafka import Consumer, KafkaException
import json

### ESEMPIO CON AUTO COMMIT CUSTOM

# Kafka configuration for consumer
consumer_config = {
    'bootstrap.servers': 'localhost:19092,localhost:29092,localhost:39092',  # Address of the Kafka broker
    'group.id': 'group1',  # Consumer group ID for managing offsets and load balancing
    'auto.offset.reset': 'earliest',  # Start reading from the earliest offset if no committed offset is found
    'enable.auto.commit': False  # Disable auto-commit to use manual offset management
}

consumer = Consumer(consumer_config)  # Initialize the Kafka consumer
to_notifier_topic = 'to-notifier'  # Topic from which the consumer will read messages
consumer.subscribe([to_notifier_topic])

sender_email = "homework2_2024@virgilio.it"
sender_password = "Agalychnis_callidry4"

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Creazione del messaggio
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Corpo del messaggio
        msg.attach(MIMEText(body, 'plain'))

        # Connessione al server SMTP
        with smtplib.SMTP('out.virgilio.it', 587) as server:
            server.starttls()  # Avvia la connessione sicura
            server.login(sender_email, sender_password)  # Autenticazione
            server.send_message(msg)  # Invio del messaggio

        print("Email inviata con successo!")

    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")

try:
    while True:
        # Poll for a new message from the Kafka topic
        msg = consumer.poll(1.0)  # Wait up to 1 second for a new message
        if msg is None:
            # No new message received within the poll interval
            continue
        if msg.error():  # Non ci sono nuovi messaggi da leggere
            # Handle any errors during message consumption
            if msg.error().code() == KafkaException._PARTITION_EOF:
                # Reached the end of the partition
                print(f"End of partition reached {msg.topic()} [{msg.partition()}]")
            else:
                # Log any other consumer errors
                print(f"Consumer error: {msg.error()}")
            continue
        
        # Parse the message value (assumed to be in JSON format)
        data = json.loads(msg.value().decode('utf-8'))

        #print(data)

        if data["condition"] == "high_value":
            body = "Dear customer\n\
                    We inform you that the value of the ticker in question has exceeded the maximum threshold you have defined.\n\
                    Kind regards,\n\
                    The Homework 2 Team."
        elif data["condition"] == "low_value":
            body = "Dear customer\n\
                    We inform you that the value of the ticker in question has dropped below the minimum threshold you have defined.\n\
                    Kind regards,\n\
                    The Homework 2 Team."
        else:
            continue
            
        #recipient_email = data["email"]
        #recipient_email = "yavifiy338@owube.com"
        recipient_email = "ceyafas663@evusd.com"
        subject = data["ticker"]

        send_email(sender_email, sender_password, recipient_email, subject, body)
        
        # Manually commit the offset for the current message
        # This ensures that the offset is only committed after processing 
        consumer.commit(asynchronous=False) # Significa che il consumer aspetta una risposta dal broker Kafka prima di proseguire.
        print(f"Committed offset for message: {msg.offset()}")  # Log the committed offset
        
        
except KeyboardInterrupt:
    # Graceful shutdown on user interruption (Ctrl+C)
    print("Consumer interrupted by user.")
finally:
    # Ensure the consumer is properly closed on exit
    consumer.close()