import mysql.connector
from mysql.connector import Error

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