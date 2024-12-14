import mysql.connector
from mysql.connector import Error
from email_verifier import is_valid_email

class RegisterUserCommand:
    def __init__(self, email: str, ticker: str, low_value: float, high_value: float):
        if not is_valid_email(email):
            raise Exception("Email not valid")
        
        self.email = email
        self.ticker = ticker
        self.low_value = low_value
        self.high_value = high_value

class UpdateTickerCommand:
    def __init__(self, email: str, ticker: str):
        if not is_valid_email(email):
            raise Exception("Email not valid")
        
        self.email = email
        self.ticker = ticker

class UpdateTickerRangeCommand:
    def __init__(self, email: str, low_value: float, high_value: float):
        if not is_valid_email(email):
            raise Exception("Email not valid")
        
        self.email = email
        self.low_value = low_value
        self.high_value = high_value

class DeleteUserCommand:
    def __init__(self, email: str):
        if not is_valid_email(email):
            raise Exception("Email not valid")
        
        self.email = email
    
class ManageUserService:
    def handle_register_user(self, command: RegisterUserCommand):
        try:
            with OpenDBConnection() as cursor:
                db_query = f"INSERT INTO users VALUES('{command.email}','{command.ticker}','{command.low_value}','{command.high_value}')"
                cursor.execute(db_query)
        except Error as e:
            print(f"Error during user registration: {e}")
            raise

    def handle_update_ticker(self, command: UpdateTickerCommand):
        try:
            with OpenDBConnection() as cursor:
                db_query = f"UPDATE users SET ticker = '{command.ticker}' WHERE email = '{command.email}'"
                cursor.execute(db_query)
        except Error as e:
            print(f"Error during ticker updating: {e}")
            raise

    def handle_update_ticker_range(self, command: UpdateTickerRangeCommand):
        try:
            with OpenDBConnection() as cursor:
                db_query = f"UPDATE users SET low_value = '{command.low_value}', high_value = '{command.high_value}' WHERE email = '{command.email}'"
                cursor.execute(db_query)
        except Error as e:
            print(f"Error during range of ticker updating: {e}")
            raise

    def handle_delete_user(self, command: DeleteUserCommand):
        try:
            with OpenDBConnection() as cursor:
                db_query = f"DELETE FROM users WHERE email = '{command.email}'"
                cursor.execute(db_query)
        except Error as e:
            print(f"Error during user account elimination: {e}")
            raise

class GetLastStockValueCommand:
    def __init__(self, email: str):
        if not is_valid_email(email):
            raise Exception("Email not valid")
        
        self.email = email

class GetStockPriceAverageCommand:
    def __init__(self, email: str, num_values: int):
        if not is_valid_email(email):
            raise Exception("Email not valid")
        
        self.email = email
        self.num_values = num_values

class StockService:
    def handle_get_last_stock_value(self, command: GetLastStockValueCommand):
        try:
            with OpenDBConnection() as cursor:
                db_query = f"SELECT\
                                d.ticker AS ticker,\
                                d.value AS last_value,\
                                d.timestamp AS last_updated\
                            FROM\
                                data d\
                            WHERE\
                                d.ticker = (\
                                    SELECT u.ticker\
                                    FROM users u\
                                    WHERE u.email = '{command.email}'\
                                )\
                                AND d.timestamp = (\
                                    SELECT MAX(d1.timestamp)\
                                    FROM data d1\
                                    WHERE d1.ticker = d.ticker\
                                )"
                cursor.execute(db_query)

                return cursor.fetchone()
        except Error as e:
            print(f"Error while getting last stock value: {e}")
            raise

    def handle_get_stock_price_average(self, command: GetStockPriceAverageCommand):
        try:
            with OpenDBConnection() as cursor:
                db_query = f"SELECT\
                                ticker,\
                                AVG(value) AS average_value,\
                                timestamp\
                            FROM (\
                                SELECT\
                                    d.ticker,\
                                    d.value,\
                                    d.timestamp\
                                FROM\
                                    data d\
                                WHERE\
                                    d.ticker = (\
                                        SELECT u.ticker\
                                        FROM users u\
                                        WHERE u.email = '{command.email}'\
                                    )\
                                ORDER BY\
                                    d.timestamp DESC\
                                LIMIT {command.num_values}\
                            ) AS filtered_data\
                            HAVING COUNT(*) = {command.num_values}"
                cursor.execute(db_query)

                return cursor.fetchone()
        except Error as e:
            print(f"Error while getting stock price average: {e}")
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
                print("Connected successfully")
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

        print("Connection closed")
