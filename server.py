from concurrent import futures
import logging
import grpc
import hw1_pb2
import hw1_pb2_grpc
import time
from threading import Lock
import mysql.connector

# A dictionary to store processed request IDs and their responses
request_cache = {}

# A lock to synchronize access to the cache for thread safety
cache_lock = Lock()

db = mysql.connector.connect(
    host="hw1_db_container",
    user="andrea",
    password="password",
    database="hw1"
)

db_cursor = db.cursor()

class ManageUserService(hw1_pb2_grpc.ManageUserServiceServicer):
    def RegisterUser(self, request: hw1_pb2.RegisterUserRequest, context) -> hw1_pb2.UserActionResponse:
        db_query = f"INSERT INTO users VALUES('{request.email}','{request.ticker}')"
        response_message = f"Email: {request.email}, Ticker: {request.ticker}"
        return at_most_once(context, db_query, response_message)
        
    def UpdateUser(self, request: hw1_pb2.UpdateUserRequest, context) -> hw1_pb2.UserActionResponse:
        db_query = f"UPDATE users SET ticker = '{request.ticker}' WHERE email = '{request.email}'"
        response_message = f"Email: {request.email}, updatedTicker: {request.ticker}"
        return at_most_once(context, db_query, response_message)
    
    def DeleteUser(self, request :hw1_pb2.DeleteUserRequest, context) -> hw1_pb2.UserActionResponse:
        db_query = f"DELETE FROM users WHERE email = '{request.email}'"
        response_message = f"Removed email: {request.email}"
        return at_most_once(context, db_query, response_message)
    
class StockService(hw1_pb2_grpc.StockServiceServicer):
    def getLastStockValue(self, request: hw1_pb2.GetLastStockValueRequest, context) -> hw1_pb2.GetLastStockValueResponse:
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
                            WHERE u.email = '{request.email}'\
                        )\
                        AND d.timestamp = (\
                            SELECT MAX(d1.timestamp)\
                            FROM data d1\
                            WHERE d1.ticker = d.ticker\
                        )"

        db_cursor.execute(db_query)

        ticker, last_value, timestamp = db_cursor.fetchone()
        response = hw1_pb2.GetLastStockValueResponse(ticker=ticker,
                                                     last_value=last_value,
                                                     timestamp=str(timestamp))
        
        return response
    
    def getStockPriceAverage(self,
                             request: hw1_pb2.GetStockPriceAverageRequest,
                             context) -> hw1_pb2.GetStockPriceAverageResponse:
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
                                WHERE u.email = '{request.email}'\
                            )\
                        ORDER BY\
                            d.timestamp DESC\
                        LIMIT {request.num_values}\
                    ) AS filtered_data\
                    HAVING COUNT(*) = {request.num_values}"
        
        db_cursor.execute(db_query)

        ticker, average_price, timestamp = db_cursor.fetchone()
        response = hw1_pb2.GetStockPriceAverageResponse(ticker=ticker,
                                                        average_price=average_price,
                                                        num_values=request.num_values,
                                                        timestamp=str(timestamp))
        
        return response
    
def at_most_once(context, query: str, response_message: str) -> hw1_pb2.UserActionResponse:
        metadata = dict(context.invocation_metadata())

        email = metadata.get('email', 'unknown')
        requestid = metadata.get('requestid', 'unknown')

        print(f"New message received - Email: {email}, RequestID: {requestid}")

        with cache_lock:
            print("Cache content:")
            for entry in request_cache:
                print(entry)

            # Check if the request ID has already been processed
            if requestid in request_cache:
                print(f"Returning cached response for RequestID {requestid}")
                # Return the cached response to ensure "at most once" processing
                return request_cache[requestid]
             
        try:
            db_cursor.execute(query)
        except Exception as e:
            print(f"MySQL error: {e}")

        db.commit()
        response = hw1_pb2.UserActionResponse(outcome=response_message)

        with cache_lock:
            request_cache[requestid] = response

        return response

def serve():
    port = '50051'
    # Initialize a thread pool with 10 workers
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Register the EchoService with the server
    hw1_pb2_grpc.add_ManageUserServiceServicer_to_server(ManageUserService(), server)
    hw1_pb2_grpc.add_StockServiceServicer_to_server(StockService(), server)
    # Bind the server to the specified port
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Echo Service started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    # Start the server without logs (no logging configuration)
    serve()
    db_cursor.close()
    db.close()
