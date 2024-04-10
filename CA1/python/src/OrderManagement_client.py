from __future__ import print_function

import logging

import grpc
import OrderManagement_pb2
import OrderManagement_pb2_grpc


def printResponseItems(response):
    for i in range(0, len(response.item)):
        print(
            "{item name: " + response.item[i] + ", Timestamp: ", response.timestamp[i] + "}")


def run():
    user_order_items = []

    while True:
        # a bug here! items like green apple are ignored cause they have spaces, fix that
        input_line = input("Enter elements separated by spaces: ")
        input_elements = input_line.split()

        if input_elements:
            user_order_items.extend(input_elements)
            break

        print("Please enter at least one element.")

    # print("Array:", user_order_items)

    with grpc.insecure_channel("localhost:50052") as channel:

        print("\n----------------------------------------------------------\n\nExecuting the unary RPC approach...\n\n")
        stub = OrderManagement_pb2_grpc.OrderManagementStub(channel)
        response = stub.getOrder(
            OrderManagement_pb2.OrderRequest(order=user_order_items))
        # check errors and size equality for two arrays - better change the response structure to array of objects
        printResponseItems(response)

        print("\n----------------------------------------------------------\n\nExecuting the client-stream approach...\n\n")

        request_iterator = iter(
            [OrderManagement_pb2.OrderRequest(order=user_order_items)])
        responseClientStream = stub.getOrderClientStream(request_iterator)
        printResponseItems(responseClientStream)


if __name__ == "__main__":
    logging.basicConfig()
    run()
