import grpc
import hw1_pb2
import hw1_pb2_grpc
import uuid #Universally Unique Identifier
import time
from functools import wraps
from email_verifier import is_valid_email

# Set the target server address
target = 'localhost:50051'

#TODO: Controllare altri codici di errore   
def send_request(request_method, request, metadata: list[tuple[str, str]] = None, timeout: int = 10):
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
            
def run():
    while(True):
        print("Insert your email, then press ENTER")
        email = input()
        if not is_valid_email(email):
            print("Please insert a valid email")
            continue

        print("Type 1 for Manage User Service, 2 for Stock Service, then press ENTER")
        service = input()
        if service == "1":
            print("Type 1 to register a new user, "
                  "2 to update an existing user, "
                  "3 to update ticker range, "
                  "4 to delete an existing user, then press ENTER")
            request = input()
            if request == "1":
                print("Insert the ticker of your interest, then press ENTER")
                ticker = input()

                print("Insert low value, then press ENTER")
                low_value = input()

                print("Insert high value, then press ENTER")
                high_value = input()

                response = manage_user(int(request), email, ticker, float(low_value), float(high_value))
                print("Response: ", response.outcome)
            elif request == "2":
                print("Insert the new ticker, then press ENTER")
                ticker = input()
                response = manage_user(int(request), email, ticker)
                print("Response: ", response.outcome)
            elif request == "3":
                print("Insert low value, then press ENTER")
                low_value = input()

                print("Insert high value, then press ENTER")
                high_value = input()

                response = manage_user(int(request), email, low_value=float(low_value), high_value=float(high_value))
                print("Response: ", response.outcome)
            elif request == "4":
                response = manage_user(int(request), email)
                print("Response: ", response.outcome)
            else:
                print("Please choose a valid option")
                continue
        elif service == "2":
            print("Type 1 to get the latest stock price, 2 to get an average stock price, then press ENTER")
            request = input()
            if request == "1":
                response = stock_service(int(request), email)
                if response is None:
                    continue

                print(f"Ticker: {response.ticker}, "
                    f"Value: {response.last_value} || "
                    f"Last updated at: {response.timestamp}")
            if request == "2":
                print("Type the number of the latest stock values to be included")
                num_values = input()
                if not num_values.isdecimal():
                    print("Please insert a number")
                    continue
            
                response = stock_service(int(request), email, int(num_values))
                if response is None:
                    continue

                print(f"Ticker: {response.ticker}, "
                    f"Average price: {response.average_price}, "
                    f"Values: {response.num_values}, || "
                    f"Last updated at {response.timestamp}")
            else:
                print("Please choose a valid option")
                continue
        else:
            print("Please choose a valid option")
            continue

            

def manage_user(request: int, email: str, ticker: str = None, low_value: float = None, high_value: float = None):
    metadata = [
        ('email', email),
        ('requestid', str(uuid.uuid4()))
    ]

    timeout = 10
    retry_attempts = 5
    for attempt in range(retry_attempts):
        with grpc.insecure_channel(target) as channel:
            stub = hw1_pb2_grpc.ManageUserServiceStub(channel)
            try:
                if(request == 1):
                    remote_request = hw1_pb2.RegisterUserRequest(email=email, ticker=ticker, low_value=low_value, high_value=high_value)
                    return stub.RegisterUser(remote_request, timeout, metadata)
                elif(request == 2):
                    remote_request = hw1_pb2.UpdateTickerRequest(email=email, ticker=ticker)
                    return stub.UpdateTicker(remote_request, timeout, metadata)
                elif(request == 3):
                    remote_request = hw1_pb2.UpdateTickerRangeRequest(email=email, low_value=low_value, high_value=high_value)
                    return stub.UpdateTickerRange(remote_request, timeout, metadata)
                elif(request == 4):
                    remote_request = hw1_pb2.DeleteUserRequest(email=email)
                    return stub.DeleteUser(remote_request, timeout, metadata)
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

    
def stock_service(request: int, email: str, num_values: int = None):
    retry_attempts = 5
    timeout = 10
    for attempt in range(retry_attempts):
        with grpc.insecure_channel(target) as channel:
            stub = hw1_pb2_grpc.StockServiceStub(channel)
            try:
                if(request == 1):
                    remote_request = hw1_pb2.GetLastStockValueRequest(email=email)
                    return stub.getLastStockValue(remote_request, timeout)
                elif(request == 2):
                    remote_request = hw1_pb2.GetStockPriceAverageRequest(email=email, num_values=num_values)
                    return stub.getStockPriceAverage(remote_request, timeout)
                    
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.CANCELLED:
                    print(e)
                    raise
                    
                # Check if the error occurred because the server is unavailable
                elif e.code() == grpc.StatusCode.UNAVAILABLE:
                    print("Server unavailable")
                    time.sleep(5)
                
                # Check if the error occurred due to a deadline (timeout) being exceeded
                elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    print("Deadline exceeded")
                    time.sleep(5)

                elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                    print(e.details())
                    return None
                
                # Handle any other type of RPC error with a generic message
                else:
                    print("posto sbagliato")
                    print(f"Received unknown RPC error: code={e.code()} message={e.details()}")
            
        if attempt < retry_attempts - 1:
            print(f"Retrying ({attempt + 1}/{retry_attempts})...")

if __name__ == '__main__':
    run()
