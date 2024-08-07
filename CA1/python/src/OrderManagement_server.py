from concurrent import futures
import logging
import time

import grpc
import OrderManagement_pb2
import OrderManagement_pb2_grpc

ServerOrders = ['banana', 'apple', 'orange', 'grape',
                'red apple', 'kiwi', 'mango', 'pear', 'cherry', 'green apple']


class OrderManager(OrderManagement_pb2_grpc.OrderManagementServicer):
    def getOrder(self, request, context):
        response = OrderManagement_pb2.OrderResponse()
        for order in request.order:
            if order in ServerOrders:
                response.item.append(order)
                response.timestamp.append(str(time.time()))
        return response

    def getOrderClientStream(self, request_iterator, context):
        response = OrderManagement_pb2.OrderResponse()
        for request in request_iterator:
            for order in request.order:
                if order in ServerOrders:
                    response.item.append(order)
                    response.timestamp.append(str(time.time()))
        return response

    def getOrderServerStream(self, request, context):
        for serverOrder in ServerOrders:
            for request_order in request.order:
                if request_order in serverOrder:
                    response = OrderManagement_pb2.OrderResponse()
                    response.item = serverOrder
                    response.timestamp = str(time.time())
                    yield response

    def getOrderBidiStream(self, request_iterator, context):
        for request in request_iterator:
            response = OrderManagement_pb2.OrderResponse()
            for order in request.order:
                if order in ServerOrders:
                    response.item = order
                    response.timestamp = str(time.time())
                    yield response


def serve():
    port = "50053"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    OrderManagement_pb2_grpc.add_OrderManagementServicer_to_server(
        OrderManager(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
