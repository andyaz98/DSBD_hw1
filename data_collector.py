import yfinance as yf
from mysql import connector
import numpy as np
import time
import random

from circuit_breaker import CircuitBreaker, CircuitBreakerOpenException

circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=5)

def data_collector():
    while(True):
        db = connector.connect(
        host="hw1_db_container",
        user="andrea",
        password="password",
        database="hw1")

        db_cursor = db.cursor()

        db_query = "SELECT DISTINCT ticker FROM users"

        db_cursor.execute(db_query)

        db_tickers = [ticker[0] for ticker in db_cursor.fetchall()]

        if len(db_tickers) == 0:
            print("There are no tickers")
            time.sleep(1)
            continue

        db_query = "INSERT INTO data (ticker, value) VALUES "
        values = []
        prices = safe_fetch_multiple_stock_prices(db_tickers)
        if prices == None:
            print("No prices for chosen tickers")
            time.sleep(1)
            continue

        for ticker, value in prices.items():
            if value is None:
                continue
            values.append(f"('{ticker}', {value})")
        db_query += ", ".join(values)

        db_cursor.execute(db_query)
        db.commit()
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