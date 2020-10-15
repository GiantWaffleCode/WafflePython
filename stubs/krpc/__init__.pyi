from typing import Any, Optional

from krpc.client import Client

DEFAULT_ADDRESS: str
DEFAULT_RPC_PORT: int
DEFAULT_STREAM_PORT: int

def connect(name: Optional[Any] = ..., address: Any = ..., rpc_port: Any = ..., stream_port: Any = ...) -> Client: ...
