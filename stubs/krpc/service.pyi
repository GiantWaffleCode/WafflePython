from krpc.types import DynamicType
from typing import Any

def create_service(client: Any, service: Any): ...

class ServiceBase(DynamicType): ...
