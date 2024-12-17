from mysql.connector import Error
from open_db_connection import OpenDBConnection

class AddValuesCommand:
    def __init__(self, prices: dict[str, float]):
        self.prices = prices

        if prices == None:
            raise Exception("No prices for chosen tickers")
    
class TickersService:
    def handle_get_tickers(self):
        try:
            with OpenDBConnection() as cursor:
                db_query = "SELECT DISTINCT ticker FROM users"
                cursor.execute(db_query)
                return cursor.fetchall()
        except Error as e:
            print(f"Error while retrieving tickers: {e}")
            raise

    def handle_add_values(self, command: AddValuesCommand):
        try:
            with OpenDBConnection() as cursor:
                db_query = "INSERT INTO data (ticker, value) VALUES "
                values = []

                for ticker, value in command.prices.items():
                    if value is None:
                        continue
                    values.append(f"('{ticker}', {value})")

                db_query += ", ".join(values)
                
                cursor.execute(db_query)
        except Error as e:
            print(f"Error while adding new values: {e}")
            raise