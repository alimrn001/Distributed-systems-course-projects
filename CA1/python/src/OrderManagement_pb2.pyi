from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OrderRequest(_message.Message):
    __slots__ = ("order",)
    ORDER_FIELD_NUMBER: _ClassVar[int]
    order: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, order: _Optional[_Iterable[str]] = ...) -> None: ...

class OrderResponse(_message.Message):
    __slots__ = ("item", "timestamp")
    ITEM_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    item: str
    timestamp: str
    def __init__(self, item: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...
