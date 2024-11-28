import grpc
import hw1_pb2
import hw1_pb2_grpc
import uuid #Universally Unique Identifier
import time
from functools import wraps

# Set the target server address
target = 'localhost:8082'

#TODO: Controllare altri codici di errore   
def send_request(request_method, request, metadata: list[tuple[str, str]] = None, timeout: int = 10):
    retry_attempts = 5
    for attempt in range(retry_attempts):
        try:
            return request_method(request, timeout, metadata)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.CANCELLED:
                print(e)
                raise
                
            # Check if the error occurred because the server is unavailable
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                print(e)
                time.sleep(5)
            
            # Check if the error occurred due to a deadline (timeout) being exceeded
            elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                print(e)
                time.sleep(5)
            
            # Handle any other type of RPC error with a generic message
            else:
                print(f"Received unknown RPC error: code={e.code()} message={e.details()}")

            if attempt < retry_attempts - 1:
                print(f"Retrying ({attempt + 1}/{retry_attempts})...")
            else:
                raise

def run():

    while(True):
        print("Type 1 for Manage User Service, 2 for Stock Service, then press ENTER")
        service = int(input())
        if (service==1):
            print("Type 1 to register a new user, 2 to update an existing user, 3 to delete an existing user, then press ENTER")
            request = int(input())
            if(request == 1):
                print("Insert your email, then press ENTER")
                email = input()
                print("Insert the ticker of your interest, then press ENTER")
                ticker=input()
                manage_user(request, email, ticker)
            elif(request == 2):
                print("Insert your email, then press ENTER")
                email = input()
                print("Insert the new ticker, then press ENTER")
                ticker = input()
                manage_user(request, email, ticker)
            elif(request == 3):
                print("Insert your email, then press ENTER")
                email=input()
                manage_user(request, email)
        elif(service == 2):
            print("Type 1 to get the latest stock price, 2 to get an average stock price, then press ENTER")
            request = int(input())
            if(request == 1):
                print("Type your email, then press ENTER")
                email = input()
                stock_service(request, email)
            if(request == 2):
                print("Type your email, then press ENTER")
                email = input()
                print("Type the number of the latest stock values to be included")
                num_values = int(input())
                stock_service(request, email, num_values)

            

def manage_user(request: int, email: str, ticker: str = None) -> None:
    metadata = [
        ('email', email),
        ('requestid', str(uuid.uuid4()))
    ]

    with grpc.insecure_channel(target) as channel:
        stub = hw1_pb2_grpc.ManageUserServiceStub(channel)
        try:
            if(request == 1):
                remote_request = hw1_pb2.RegisterUserRequest(email=email, ticker=ticker)
                response = send_request(stub.RegisterUser, remote_request, metadata)
                print("Response: ", response.outcome)
            elif(request == 2):
                remote_request = hw1_pb2.RegisterUserRequest(email=email, ticker=ticker)
                response = send_request(stub.UpdateUser, remote_request, metadata)
                print("Response: ", response.outcome)
            elif(request == 3):
                remote_request = hw1_pb2.DeleteUserRequest(email=email)
                response = send_request(stub.DeleteUser, remote_request, metadata)
                print("Response: ", response.outcome)
        
        except Exception as e:
            print(e)

    
def stock_service(request: int, email: str, num_values: int = None) -> None:
    with grpc.insecure_channel(target) as channel:
        stub = hw1_pb2_grpc.StockServiceStub(channel)
        try:
            if(request == 1):
                remote_request = hw1_pb2.GetLastStockValueRequest(email=email)
                response = send_request(stub.getLastStockValue, remote_request)
                print(f"Ticker: {response.ticker}, "
                f"Value: {response.last_value} || "
                f"Last updated at: {response.timestamp}")
            elif(request == 2):
                remote_request = hw1_pb2.GetStockPriceAverageRequest(email=email, num_values=num_values)
                response = send_request(stub.getStockPriceAverage, remote_request)
                print(f"Ticker: {response.ticker}, "
                f"Average price: {response.average_price}, "
                f"Values: {response.num_values}, || "
                f"Last updated at {response.timestamp}")

        except Exception as e:
            print(e)

if __name__ == '__main__':
    run()
