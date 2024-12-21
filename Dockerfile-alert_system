FROM python:3.13

WORKDIR /app

COPY alert_system.py /app/
COPY cqrs_alert_system.py  /app/
COPY produce_sync.py /app/
COPY open_db_connection.py /app/

RUN pip install confluent-kafka mysql-connector-python

CMD python alert_system.py
