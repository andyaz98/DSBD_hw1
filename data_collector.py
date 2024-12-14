import yfinance as yf
import numpy as np
import time
import random
import cqrs_data_collector

from circuit_breaker import CircuitBreaker, CircuitBreakerOpenException

circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=5)

def data_collector():
    tickers_service = cqrs_data_collector.TickersService()

    while(True):
        try:
            db_tickers = [ticker[0] for ticker in tickers_service.handle_get_tickers()]

            if len(db_tickers) == 0:
                print("There are no tickers")
                time.sleep(1)
                continue

            prices = safe_fetch_multiple_stock_prices(db_tickers)

            add_values_command = cqrs_data_collector.AddValuesCommand(prices)

            tickers_service.handle_add_values(add_values_command)
        except:
            time.sleep(1)
            continue

        time.sleep(30 * 60) #Every 30 minutes

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

if __name__ == "__main__":
    data_collector()