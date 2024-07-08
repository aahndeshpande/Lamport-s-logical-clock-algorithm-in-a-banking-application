from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MsgDeliveryRequest(_message.Message):
    __slots__ = ["id", "event_id", "interface", "money", "balance", "logical_clock", "bank_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    LOGICAL_CLOCK_FIELD_NUMBER: _ClassVar[int]
    BANK_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    event_id: int
    interface: str
    money: int
    balance: int
    logical_clock: int
    bank_id: int
    def __init__(self, id: _Optional[int] = ..., event_id: _Optional[int] = ..., interface: _Optional[str] = ..., money: _Optional[int] = ..., balance: _Optional[int] = ..., logical_clock: _Optional[int] = ..., bank_id: _Optional[int] = ...) -> None: ...

class MsgDeliveryResponse(_message.Message):
    __slots__ = ["id", "event_id", "bank_id", "balance", "result", "logical_clock"]
    ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    BANK_ID_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    LOGICAL_CLOCK_FIELD_NUMBER: _ClassVar[int]
    id: int
    event_id: int
    bank_id: int
    balance: int
    result: str
    logical_clock: int
    def __init__(self, id: _Optional[int] = ..., event_id: _Optional[int] = ..., bank_id: _Optional[int] = ..., balance: _Optional[int] = ..., result: _Optional[str] = ..., logical_clock: _Optional[int] = ...) -> None: ...
