FROM python:3.13

WORKDIR /app

COPY alert_notifier_system.py /app/

RUN pip install confluent_kafka

CMD python alert_notifier_system.py
