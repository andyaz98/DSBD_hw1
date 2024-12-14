import mysql.connector
from mysql.connector import Error

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

class OpenDBConnection:
    def __init__(self,
                 host: str = "localhost",
                 user: str = "andrea",
                 password: str = "password",
                 database: str = "hw1"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                return self.cursor
        except Error as e:
            print(f"Error during connection: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None: # No exceptions
            try:
                self.connection.commit()
            except Error as e:
                print(f"Error during commit: {e}")

        else: # Exception occurred
            print(f"Error during the execution of the query: {exc_val}")
            try:
                self.connection.rollback()
            except Error as e:
                print(f"Error during rollback: {e}")

        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
