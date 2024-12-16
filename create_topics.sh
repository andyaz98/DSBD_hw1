#!/bin/bash

kafka-topics --create --topic to-alert-system --partitions 1 --replication-factor 3 --if-not-exists --bootstrap-server localhost:9092
kafka-topics --create --topic to-notifier --partitions 1 --replication-factor 3 --if-not-exists --bootstrap-server localhost:9092

echo "Topic creati con successo."