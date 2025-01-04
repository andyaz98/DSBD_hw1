import yfinance as yf
import numpy as np
import time
import random
import cqrs_data_collector
from circuit_breaker import CircuitBreaker, CircuitBreakerOpenException
from confluent_kafka import Producer
import json
from datetime import datetime
from produce_sync import produce_sync
import data_collector_exporter

time.sleep(30)

circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=5)

producer_config = {
    # NB: se il producer viene inserito in un container va messo come indirizzo -> '<container_name>:<porta definita in PLAINTEXT>' es. 'kafka:9092'
    'bootstrap.servers': 'broker-1:9092,broker-2:9093,broker-3:9094',  # Kafka broker address
    'acks': 'all',  # Ensure all in-sync replicas acknowledge the message
    'batch.size': 500,  # Maximum number of bytes to batch in a single request
    'max.in.flight.requests.per.connection': 1,  # Only one in-flight request per connection
    'retries': 3  # Retry up to 3 times on failure
}

producer = Producer(producer_config)
topic = 'to-alert-system'  # Topic to produce messages to

def data_collector():
    tickers_service = cqrs_data_collector.TickersService()

    while(True):
        try:
            db_tickers = [ticker[0] for ticker in tickers_service.handle_get_tickers()]

            if len(db_tickers) == 0:
                print("There are no tickers")
                time.sleep(1)
                continue

            start = time.time()
            

            prices = safe_fetch_multiple_stock_prices(db_tickers)
            add_values_command = cqrs_data_collector.AddValuesCommand(prices)
            tickers_service.handle_add_values(add_values_command)

            end = time.time()
            duration = end - start
            data_collector_exporter.UPDATE_TIME.labels(service='data_collector', node=data_collector_exporter.HOSTNAME).set(duration)
        except:
            data_collector_exporter.ERROR_COUNT.labels(service="data_collector", node=data_collector_exporter.HOSTNAME).inc()
            time.sleep(1)
            continue

        timestamp = datetime.now().isoformat() 
        message = {'timestamp': timestamp, 'updated_tickers': True}

        produce_sync(producer, topic, json.dumps(message))
        
        time.sleep(30 * 60) #Every 30 minutes
        #time.sleep(1)

def fetch_multiple_stock_prices(tickers: list[str]) -> dict[str, np.float64]:
    #Test 
    """ if random.random() < 0.5:
        raise Exception("Test Exception") """
    
    data = yf.download(tickers, period="1d", group_by="ticker")
    prices = {}

    for ticker in tickers:
        try:
            prices[ticker] = data[ticker]["Close"].at[data[ticker].index[-1]]
        except KeyError:
            prices[ticker] = None

    return prices

def safe_fetch_multiple_stock_prices(ticker: str) -> dict[str, np.float64]:
    for i in range(20):
        try:
            return circuit_breaker.call(fetch_multiple_stock_prices, ticker)
        except CircuitBreakerOpenException:
            print(f"Call {i}: Circuit is open, skipping call.")
        except Exception as e:
            print(f"Call {i}: {e}")

def delivery_report(err, msg):
    """Callback to report the result of message delivery."""
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

if __name__ == "__main__":
    data_collector()
    