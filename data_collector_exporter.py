import prometheus_client  # Prometheus Python client library
import socket  # Used to fetch the hostname

prometheus_client.start_http_server(7777)

# Fetch the hostname dynamically
HOSTNAME = socket.gethostname()

UPDATE_TIME = prometheus_client.Gauge(
    'update_time', 
    'time elapsed to update the tickers',
    ['service', 'node']
)

ERROR_COUNT = prometheus_client.Counter(
    'error_count', 
    'count of errors occurred while fetching data from db and yfinance', 
    ['service', 'node']
)

