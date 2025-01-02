FROM python:3.13

WORKDIR /app

COPY server.py /app/
COPY email_verifier.py /app/
COPY hw1_pb2_grpc.py /app/
COPY hw1_pb2.py /app/
COPY hw1_pb2.pyi /app/
COPY cqrs_server.py /app/
COPY open_db_connection.py /app/
COPY server_exporter.py /app/

RUN pip install grpcio grpcio-tools google-api-python-client mysql-connector-python prometheus_client
CMD python server.py


