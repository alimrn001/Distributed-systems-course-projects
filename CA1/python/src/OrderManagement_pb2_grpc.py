# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import OrderManagement_pb2 as OrderManagement__pb2


class OrderManagementStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getOrder = channel.unary_unary(
                '/order_management.OrderManagement/getOrder',
                request_serializer=OrderManagement__pb2.OrderRequest.SerializeToString,
                response_deserializer=OrderManagement__pb2.OrderResponse.FromString,
                )
        self.getOrderClientStream = channel.stream_unary(
                '/order_management.OrderManagement/getOrderClientStream',
                request_serializer=OrderManagement__pb2.OrderRequest.SerializeToString,
                response_deserializer=OrderManagement__pb2.OrderResponse.FromString,
                )
        self.getOrderServerStream = channel.unary_stream(
                '/order_management.OrderManagement/getOrderServerStream',
                request_serializer=OrderManagement__pb2.OrderRequest.SerializeToString,
                response_deserializer=OrderManagement__pb2.OrderResponse.FromString,
                )
        self.getOrderBidiStream = channel.stream_stream(
                '/order_management.OrderManagement/getOrderBidiStream',
                request_serializer=OrderManagement__pb2.OrderRequest.SerializeToString,
                response_deserializer=OrderManagement__pb2.OrderResponse.FromString,
                )


class OrderManagementServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getOrderClientStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getOrderServerStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getOrderBidiStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderManagementServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.getOrder,
                    request_deserializer=OrderManagement__pb2.OrderRequest.FromString,
                    response_serializer=OrderManagement__pb2.OrderResponse.SerializeToString,
            ),
            'getOrderClientStream': grpc.stream_unary_rpc_method_handler(
                    servicer.getOrderClientStream,
                    request_deserializer=OrderManagement__pb2.OrderRequest.FromString,
                    response_serializer=OrderManagement__pb2.OrderResponse.SerializeToString,
            ),
            'getOrderServerStream': grpc.unary_stream_rpc_method_handler(
                    servicer.getOrderServerStream,
                    request_deserializer=OrderManagement__pb2.OrderRequest.FromString,
                    response_serializer=OrderManagement__pb2.OrderResponse.SerializeToString,
            ),
            'getOrderBidiStream': grpc.stream_stream_rpc_method_handler(
                    servicer.getOrderBidiStream,
                    request_deserializer=OrderManagement__pb2.OrderRequest.FromString,
                    response_serializer=OrderManagement__pb2.OrderResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'order_management.OrderManagement', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OrderManagement(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/order_management.OrderManagement/getOrder',
            OrderManagement__pb2.OrderRequest.SerializeToString,
            OrderManagement__pb2.OrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getOrderClientStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/order_management.OrderManagement/getOrderClientStream',
            OrderManagement__pb2.OrderRequest.SerializeToString,
            OrderManagement__pb2.OrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getOrderServerStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/order_management.OrderManagement/getOrderServerStream',
            OrderManagement__pb2.OrderRequest.SerializeToString,
            OrderManagement__pb2.OrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getOrderBidiStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/order_management.OrderManagement/getOrderBidiStream',
            OrderManagement__pb2.OrderRequest.SerializeToString,
            OrderManagement__pb2.OrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
