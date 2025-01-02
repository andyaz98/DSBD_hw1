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