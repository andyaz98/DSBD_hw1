FROM python:3.13

WORKDIR /app

COPY create_topics.py /app

RUN pip install confluent_kafka
EXPOSE 2222
CMD python create_topics.py


