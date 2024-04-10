from __future__ import print_function

import logging

import grpc
import OrderManagement_pb2
import OrderManagement_pb2_grpc


def run():
    user_order_items = []

    while True:
        input_line = input("Enter elements separated by spaces: ")
        input_elements = input_line.split()

        if input_elements:
            user_order_items.extend(input_elements)
            break

        print("Please enter at least one element.")

    print("Array:", user_order_items)

    with grpc.insecure_channel("localhost:50052") as channel:
        stub = OrderManagement_pb2_grpc.OrderManagementStub(channel)
        response = stub.getOrder(
            OrderManagement_pb2.OrderRequest(order=user_order_items))
        print("Order item:", response.item)
        print("Timestamp:", response.timestamp)


if __name__ == "__main__":
    logging.basicConfig()
    run()
