FROM python:3.13

WORKDIR /app

COPY circuit_breaker.py /app/
COPY data_collector.py /app/
COPY cqrs_data_collector.py /app/
COPY open_db_connection.py /app/
COPY produce_sync.py /app/
COPY data_collector_exporter.py /app/

RUN pip install yfinance mysql-connector-python confluent-kafka numpy prometheus_client

CMD python data_collector.py
