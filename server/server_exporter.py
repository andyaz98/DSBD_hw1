import prometheus_client  # Prometheus Python client library
import socket  # Used to fetch the hostname

prometheus_client.start_http_server(5555)

# Fetch the hostname dynamically
HOSTNAME = socket.gethostname()

REQUESTS_COUNT = prometheus_client.Counter(
    'requests_count', 
    'Number of requests from clients',
    ['service', 'node']
)

RESPONSE_TIME_GET_STOCK_PRICE_AVERAGE = prometheus_client.Gauge(
    'response_time_get_stock_price_average', 
    'time elapsed to get stock price average',
    ['service', 'node']
)

