# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = data_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x

def from_float(x: Any) -> float:
    assert isinstance(x, float) and not isinstance(x, bool)
    return x

def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Data:
    server: str
    memory_used: str
    total_mem: str
    disk_percent: float
    cpu_percent: float

    def __init__(self, server: str) -> None:
        self.server = server

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        server = from_str(obj.get("server"))
        memory_used = from_str(obj.get("memory_used"))
        total_mem = from_str(obj.get("total_mem"))
        disk_percent = from_float(obj.get("disk_percent"))
        cpu_percent = from_float(obj.get("cpu_percent"))
        return Data(server, memory_used, total_mem, disk_percent, cpu_percent)

    def to_dict(self) -> dict:
        result: dict = {}
        result["server"] = from_str(self.server)
        result["memory_used"] = from_str(self.memory_used)
        result["total_mem"] = from_str(self.total_mem)
        result["disk_percent"] = from_float(self.disk_percent)
        result["cpu_percent"] = from_float(self.cpu_percent)
        return result


def data_from_dict(s: Any) -> Data:
    return Data.from_dict(s)


def data_to_dict(x: Data) -> Any:
    return to_class(Data, x)
