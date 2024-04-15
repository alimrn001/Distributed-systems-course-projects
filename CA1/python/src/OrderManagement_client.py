import logging
import grpc
import OrderManagement_pb2
import OrderManagement_pb2_grpc

def getUserOrderListAsInput():
    user_order_items = input("Enter elements separated by commas and space afterwards: ")
    return [item.strip() for item in user_order_items.split(",") if item.strip()]

def getOrderServerStream(stub):
    user_order_item = input("Enter item name: ")
    responseServerStream = stub.getOrderServerStream(OrderManagement_pb2.OrderRequest(order=[user_order_item]))
    for serverStreamResponseItem in responseServerStream:
        print(f"Item name: {serverStreamResponseItem.item}, Timestamp: {serverStreamResponseItem.timestamp}")

def getOrderBidiStream(stub):
    user_order_items = getUserOrderListAsInput()
    request_iterator_bidi = (OrderManagement_pb2.OrderRequest(order=[item]) for item in user_order_items)
    responseBidiStream = stub.getOrderBidiStream(request_iterator_bidi)
    for serverStreamResponseItem in responseBidiStream:
        print(f"Item name: {serverStreamResponseItem.item}, Timestamp: {serverStreamResponseItem.timestamp}")

def run():
    with grpc.insecure_channel("localhost:50053") as channel:
        stub = OrderManagement_pb2_grpc.OrderManagementStub(channel)
        communication_pattern_selector = input("Please select your communication pattern.\n Press [0] for server-streaming RPC, or press [1] for bidirectional streaming RPC: ")
        if communication_pattern_selector == "0":
            getOrderServerStream(stub)
        elif communication_pattern_selector == "1":
            getOrderBidiStream(stub)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    logging.basicConfig()
    run()
