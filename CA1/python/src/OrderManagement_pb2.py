# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: OrderManagement.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15OrderManagement.proto\x12\x10order_management\"\x1d\n\x0cOrderRequest\x12\r\n\x05order\x18\x01 \x03(\t\"0\n\rOrderResponse\x12\x0c\n\x04item\x18\x01 \x03(\t\x12\x11\n\ttimestamp\x18\x02 \x03(\t2\xef\x02\n\x0fOrderManagement\x12K\n\x08getOrder\x12\x1e.order_management.OrderRequest\x1a\x1f.order_management.OrderResponse\x12Y\n\x14getOrderClientStream\x12\x1e.order_management.OrderRequest\x1a\x1f.order_management.OrderResponse(\x01\x12Y\n\x14getOrderServerStream\x12\x1e.order_management.OrderRequest\x1a\x1f.order_management.OrderResponse0\x01\x12Y\n\x12getOrderBidiStream\x12\x1e.order_management.OrderRequest\x1a\x1f.order_management.OrderResponse(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'OrderManagement_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ORDERREQUEST']._serialized_start=43
  _globals['_ORDERREQUEST']._serialized_end=72
  _globals['_ORDERRESPONSE']._serialized_start=74
  _globals['_ORDERRESPONSE']._serialized_end=122
  _globals['_ORDERMANAGEMENT']._serialized_start=125
  _globals['_ORDERMANAGEMENT']._serialized_end=492
# @@protoc_insertion_point(module_scope)
