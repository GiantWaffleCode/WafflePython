from typing import Any, Optional

class Stream:
    def __init__(self, stream: Any) -> None: ...
    @classmethod
    def from_stream_id(cls, conn: Any, stream_id: Any, return_type: Any): ...
    @classmethod
    def from_call(cls, conn: Any, return_type: Any, call: Any): ...
    def start(self, wait: bool = ...) -> None: ...
    @property
    def rate(self): ...
    @rate.setter
    def rate(self, value: Any) -> None: ...
    def __call__(self): ...
    @property
    def condition(self): ...
    def wait(self, timeout: Optional[Any] = ...) -> None: ...
    def add_callback(self, callback: Any) -> None: ...
    def remove_callback(self, callback: Any) -> None: ...
    def remove(self) -> None: ...