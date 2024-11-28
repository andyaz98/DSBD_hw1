import grpc
import hw1_pb2
import hw1_pb2_grpc
import uuid #Universally Unique Identifier
import time
from functools import wraps

#TODO: Controllare altri codici di errore   
def send_request(request_method, request, metadata: list[tuple[str, str]] = None, timeout: int = 10):
    retry_attempts = 1
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
    # Set the target server address
    target = 'localhost:50051'
    
    email = "claude@icio.com"
    #requestid = uuid.uuid4()
    requestid = 8

    # Convert long integers to strings, as metadata values must be strings
    metadata = [
        ('email', email),
        ('requestid', str(requestid))
    ]

    # Establish a connection to the gRPC server

    with grpc.insecure_channel(target) as channel:
        # Create a stub (client) for the EchoService
        stub = hw1_pb2_grpc.ManageUserStub(channel)
        registerRequest = hw1_pb2.Register(email="alchemai@deleit.com", ticker="icio")
        updateRequest = hw1_pb2.Update(email="pluto@icio.com", ticker="ocio")
        deleteRequest = hw1_pb2.Delete(email="prova@icio.com")

        try:
            registerResponse = send_request(stub.RegisterMessage, registerRequest, metadata)
            print("Response: ", registerResponse.outcome)

            """ updateResponse = send_request(stub.UpdateMessage, updateRequest, metadata)
            print("Response: ", updateResponse.outcome)

            deleteResponse = send_request(stub.DeleteMessage, deleteRequest, metadata)
            print("Response: ", deleteResponse.outcome) """

        except:
            print("Service 1 test: failed after too many attempts")

        stub = hw1_pb2_grpc.StockServiceStub(channel)
        last_stock_value_request = hw1_pb2.GetLastStockValueRequest(email="claude@icio.com")

        try:
            last_stock_value = send_request(stub.getLastStockValue, last_stock_value_request)
            print(f"Ticker: {last_stock_value.ticker}, "
                  f"Value: {last_stock_value.last_value} || "
                  f"Last updated at: {last_stock_value.timestamp}")
        except Exception as e:
            print(e)

        stock_price_average_request = hw1_pb2.GetStockPriceAverageRequest(email="alchemai@deleit.com", num_values=3)

        try:
            stock_price_average = send_request(stub.getStockPriceAverage, stock_price_average_request)
            print(f"Ticker: {stock_price_average.ticker}, "
                  f"Average price: {stock_price_average.average_price}, "
                  f"Values: {stock_price_average.num_values}, || "
                  f"Last updated at {stock_price_average.timestamp}")
        except Exception as e: 
            print(e)

if __name__ == '__main__':
    run()
