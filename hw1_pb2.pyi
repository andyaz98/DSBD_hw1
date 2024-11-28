from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterUserRequest(_message.Message):
    __slots__ = ("email", "ticker")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    email: str
    ticker: str
    def __init__(self, email: _Optional[str] = ..., ticker: _Optional[str] = ...) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ("email", "ticker")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    email: str
    ticker: str
    def __init__(self, email: _Optional[str] = ..., ticker: _Optional[str] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class UserActionResponse(_message.Message):
    __slots__ = ("outcome",)
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    outcome: str
    def __init__(self, outcome: _Optional[str] = ...) -> None: ...

class GetLastStockValueRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class GetLastStockValueResponse(_message.Message):
    __slots__ = ("ticker", "last_value", "timestamp")
    TICKER_FIELD_NUMBER: _ClassVar[int]
    LAST_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ticker: str
    last_value: float
    timestamp: str
    def __init__(self, ticker: _Optional[str] = ..., last_value: _Optional[float] = ..., timestamp: _Optional[str] = ...) -> None: ...

class GetStockPriceAverageRequest(_message.Message):
    __slots__ = ("email", "num_values")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NUM_VALUES_FIELD_NUMBER: _ClassVar[int]
    email: str
    num_values: int
    def __init__(self, email: _Optional[str] = ..., num_values: _Optional[int] = ...) -> None: ...

class GetStockPriceAverageResponse(_message.Message):
    __slots__ = ("ticker", "average_price", "num_values", "timestamp")
    TICKER_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_PRICE_FIELD_NUMBER: _ClassVar[int]
    NUM_VALUES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ticker: str
    average_price: float
    num_values: int
    timestamp: str
    def __init__(self, ticker: _Optional[str] = ..., average_price: _Optional[float] = ..., num_values: _Optional[int] = ..., timestamp: _Optional[str] = ...) -> None: ...
