import prometheus_client  # Prometheus Python client library
import time  # Used to control the update interval for metrics
#import psutil  # Can be used for real system metrics if needed
import random  # Generates random values for simulated metrics
import socket  # Used to fetch the hostname

prometheus_client.start_http_server(5555)

# Update interval in seconds
UPDATE_PERIOD = 30

# Fetch the hostname dynamically
HOSTNAME = socket.gethostname()

# Application name label
APP_NAME = "random_exporter"

# Prometheus Gauge metric for fake CPU usage, with server, hostname, and app as labels
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

""" # Prometheus Counter metric for number of iterations, with server, hostname, and app as labels
NUM_ITERATION = prometheus_client.Counter(
    'system_usage', 
    'Real iterations value', 
    ['server', 'hostname', 'app']
) """

""" if __name__ == '__main__':
    # Start the Prometheus HTTP server on port 9999
    prometheus_client.start_http_server(9999)
    print(f"Prometheus metrics are available at http://{HOSTNAME}:9999/metrics")

    # Infinite loop to update metrics at each interval
    while True:
        # Set a random value for CPU usage
        CPU_RANDOM_USAGE.labels(server='random-node', hostname=HOSTNAME, app=APP_NAME).set(random.random() * 100)

        # Set a random value for memory usage
        MEM_RANDOM_USAGE.labels(server='random-node', hostname=HOSTNAME, app=APP_NAME).set(random.random() * 100)

        # Set a random value for response time using a Gaussian distribution
        RESPONSE_TIME_RANDOM.labels(server='random-node', hostname=HOSTNAME, app=APP_NAME).set(random.gauss(mu=125.0, sigma=30.0))

        # Increment the iteration counter
        NUM_ITERATION.labels(server='random-node', hostname=HOSTNAME, app=APP_NAME).inc()

        # Wait for the next update
        time.sleep(UPDATE_PERIOD) """