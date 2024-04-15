from __future__ import print_function

import logging
import time
import grpc
import OrderManagement_pb2
import OrderManagement_pb2_grpc


def printResponseItems(response):
    for item, timestamp in zip(response.item, response.timestamp):
        print(f"Item name: {item}, Timestamp: {timestamp}")
    
    # print(len(response))
    # for i in range(0, len(response.item)):
    #     print(
    #         "{item name: " + response.item[i] + ", Timestamp: ", response.timestamp[i] + "}")

def getUserOrderListAsInput():
    user_order_items = []
    while True:
        input_line = input("Enter elements separated by commas and space afterwards: ")
        input_elements = input_line.split(", ")
        if input_elements:
            user_order_items.extend(input_elements)
            break
        print("Please enter at least one element.")
    return user_order_items

def getOrderServerStream(stub):
    user_order_item = input("enter your item name:")
    responseServerStream = stub.getOrderServerStream(OrderManagement_pb2.OrderRequest(order=user_order_item))
    for serverStreamResponseItem in responseServerStream:
        print(serverStreamResponseItem)


def getOrderBidiStream(stub):
    user_order_items = getUserOrderListAsInput()
    request_iterator_bidi = (OrderManagement_pb2.OrderRequest(order=item) for item in user_order_items)
    responseBidiStream = stub.getOrderBidiStream(request_iterator_bidi)
    for serverStreamResponseItem in responseBidiStream:
        printResponseItems(serverStreamResponseItem)

def run():
    # user_order_items = []

    while True:
        communication_pattern_selector = input("Please select your communication pattern.\n Press [0] for server-streaming RPC, or press [1] for bidirectional streaming RPC.")
        if communication_pattern_selector == "0" or communication_pattern_selector == "1":
            break
    
    

    with grpc.insecure_channel("localhost:50052") as channel:

        # print("\n----------------------------------------------------------\n\nExecuting the unary RPC approach...\n\n")
        stub = OrderManagement_pb2_grpc.OrderManagementStub(channel)
        
        if(communication_pattern_selector == "0"):
            getOrderServerStream(stub)
        elif(communication_pattern_selector == "1"):
            getOrderBidiStream(stub)
        
        # response = stub.getOrder(
        #     OrderManagement_pb2.OrderRequest(order=user_order_items))
        # # check errors and size equality for two arrays - better change the response structure to array of objects
        # printResponseItems(response)

        # print("\n----------------------------------------------------------\n\nExecuting the client-stream approach...\n\n")

        # request_iterator = iter(
        #     [OrderManagement_pb2.OrderRequest(order=user_order_items)])
        # responseClientStream = stub.getOrderClientStream(request_iterator)
        # printResponseItems(responseClientStream)

        # print("\n----------------------------------------------------------\n\nExecuting the server-stream approach...\n\n")

        # responseServerStream = stub.getOrderServerStream(
        #     OrderManagement_pb2.OrderRequest(order=user_order_items[0]))
        # print(responseServerStream)
        # for serverStreamResponseItem in responseServerStream:
        #     print(serverStreamResponseItem)
        #     printResponseItems(serverStreamResponseItem)

        # print("\n----------------------------------------------------------\n\nExecuting the bidirectional-stream approach...\n\n")
        # request_iterator_bidi = iter(
        #     [OrderManagement_pb2.OrderRequest(order=user_order_items)])
        # print("oder items: ")
        # print([OrderManagement_pb2.OrderRequest(order=user_order_items)])
        # print(len(list(request_iterator_bidi)))
        # cnt = 0
        # responseBidiStream = stub.getOrderBidiStream(
        #     request_iterator_bidi)  # bug: response is empty!
        # for serverStreamResponseItem in responseBidiStream:
        #     printResponseItems(serverStreamResponseItem)


if __name__ == "__main__":
    logging.basicConfig()
    run()
