from concurrent import futures
import logging
import grpc
import hw1_pb2
import hw1_pb2_grpc
import time
from threading import Lock
import mysql.connector
from email_verifier import is_valid_email
import CQRS

# A lock to synchronize access to the cache for thread safety
cache_lock = Lock()

class ManageUserService(hw1_pb2_grpc.ManageUserServiceServicer):
    def __init__(self):
        self.manage_user_service = CQRS.ManageUserService()
        self.request_cache = {} # A dictionary to store processed request IDs and their responses

    def RegisterUser(self, request: hw1_pb2.RegisterUserRequest, context) -> hw1_pb2.UserActionResponse:
        try:
            register_user_command = CQRS.RegisterUserCommand(request.email, request.ticker, request.low_value, request.high_value)

            response_message = f"Email: {request.email}, Ticker: {request.ticker}, Low value: {request.low_value}, High value: {request.high_value}"
            return at_most_once(context, self.request_cache, self.manage_user_service.handle_register_user, register_user_command, response_message)
        except:
            raise
        
    def UpdateTicker(self, request: hw1_pb2.UpdateTickerRequest, context) -> hw1_pb2.UserActionResponse:
        try:
            update_ticker_command = CQRS.UpdateTickerCommand(request.email, request.ticker)

            response_message = f"Email: {request.email}, Ticker: {request.ticker}"
            return at_most_once(context, self.request_cache, self.manage_user_service.handle_update_ticker, update_ticker_command, response_message)
        except:
            raise
    
    def UpdateTickerRange(self, request: hw1_pb2.UpdateTickerRangeRequest, context) -> hw1_pb2.UserActionResponse:
        try:
            update_ticker_range_command = CQRS.UpdateTickerRangeCommand(request.email, request.low_value, request.high_value)

            response_message = f"Email: {request.email}, Low value: {request.low_value}, High value: {request.high_value}"
            return at_most_once(context, self.request_cache, self.manage_user_service.handle_update_ticker_range, update_ticker_range_command, response_message)
        except:
            raise
    
    def DeleteUser(self, request :hw1_pb2.DeleteUserRequest, context) -> hw1_pb2.UserActionResponse:
        try:
            delete_user_command = CQRS.DeleteUserCommand(request.email)

            response_message = f"Removed Email: {request.email}"
            return at_most_once(context, self.request_cache, self.manage_user_service.handle_delete_user, delete_user_command, response_message)
        except:
            raise
    
class StockService(hw1_pb2_grpc.StockServiceServicer):
    def __init__(self):
        self.stock_service = CQRS.StockService()

    def getLastStockValue(self, request: hw1_pb2.GetLastStockValueRequest, context) -> hw1_pb2.GetLastStockValueResponse:
        try:
            get_last_stock_value_command = CQRS.GetLastStockValueCommand(request.email)
            row = self.stock_service.handle_get_last_stock_value(get_last_stock_value_command)
        except:
            raise

        if row is None:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "No value found")
        
        ticker, last_value, timestamp = row
        response = hw1_pb2.GetLastStockValueResponse(ticker=ticker,
                                                     last_value=last_value,
                                                     timestamp=str(timestamp))
        
        return response
    
    def getStockPriceAverage(self,
                             request: hw1_pb2.GetStockPriceAverageRequest,
                             context) -> hw1_pb2.GetStockPriceAverageResponse:
        try:
            get_stock_price_average_command = CQRS.GetStockPriceAverageCommand(request.email, request.num_values)
            row = self.stock_service.handle_get_stock_price_average(get_stock_price_average_command)
        except:
            raise

        if row is None:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Insufficient number of values")
        
        ticker, average_price, timestamp = row

        response = hw1_pb2.GetStockPriceAverageResponse(ticker=ticker,
                                                        average_price=average_price,
                                                        num_values=request.num_values,
                                                        timestamp=str(timestamp))
        
        return response
    
def at_most_once(context, request_cache: dict[str, hw1_pb2.UserActionResponse], handle_function, command, response_message: str) -> hw1_pb2.UserActionResponse:
        metadata = dict(context.invocation_metadata())

        email = metadata.get('email', 'unknown')
        requestid = metadata.get('requestid', 'unknown')

        print(f"New message received - Email: {email}, RequestID: {requestid}")

        with cache_lock:
            # Check if the request ID has already been processed
            if requestid in request_cache:
                print(f"Returning cached response for RequestID {requestid}")
                # Return the cached response to ensure "at most once" processing
                return request_cache[requestid]
             
        handle_function(command)

        response = hw1_pb2.UserActionResponse(outcome=response_message)

        with cache_lock:
            request_cache[requestid] = response

            print("Cache content:")
            for entry in request_cache:
                print(entry)
            print("\n")

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
    print("Service started, listening on " + port)
    server.wait_for_termination()

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="andrea",
        password="password",
        database="hw1"
    )

if __name__ == '__main__':
    # Start the server without logs (no logging configuration)
    serve()
