from mysql.connector import Error
from open_db_connection import OpenDBConnection

class FindUsersToNotifyService:
    def handle_get_users(self):
        try:
            with OpenDBConnection() as cursor:
                db_query = "SELECT\
                                u.email,\
                                u.ticker,\
                                CASE\
                                    WHEN d.value > u.high_value THEN 'high_value'\
                                    WHEN d.value < u.low_value THEN 'low_value'\
                                END AS threshold\
                            FROM\
                                users u\
                            JOIN\
                                (SELECT\
                                    ticker,\
                                    value,\
                                    timestamp\
                                FROM\
                                    data d1\
                                WHERE\
                                    timestamp = (SELECT MAX(d2.timestamp)\
                                                FROM data d2\
                                                WHERE d2.ticker = d1.ticker)\
                                ) d\
                            ON\
                                u.ticker = d.ticker\
                            WHERE\
                                d.value > u.high_value\
                                OR\
                                d.value < u.low_value"

                cursor.execute(db_query)
                return cursor.fetchall()
        except Error as e:
            print(f"Error while retrieving users to notify: {e}")
            raise
