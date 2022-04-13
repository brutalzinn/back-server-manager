# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = data_from_dict(json.loads(json_string))

from typing import Optional, Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Data:
    server: Optional[str]
    memory_used: Optional[str]
    total_mem: Optional[str]
    disk_percent: Optional[float]
    cpu_percent: Optional[float]
    cpu_frequency: Optional[float]

    def __init__(self, server: Optional[str]) -> None:
        self.server = server
  

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        server = from_union([from_str, from_none], obj.get("server"))
        memory_used = from_union([from_str, from_none], obj.get("memory_used"))
        total_mem = from_union([from_str, from_none], obj.get("total_mem"))
        disk_percent = from_union([from_float, from_none], obj.get("disk_percent"))
        cpu_percent = from_union([from_float, from_none], obj.get("cpu_percent"))
        cpu_frequency = from_union([from_float, from_none], obj.get("cpu_frequency"))
        return Data(server, memory_used, total_mem, disk_percent, cpu_percent, cpu_frequency)

    def to_dict(self) -> dict:
        result: dict = {}
        result["server"] = from_union([from_str, from_none], self.server)
        result["memory_used"] = from_union([from_str, from_none], self.memory_used)
        result["total_mem"] = from_union([from_str, from_none], self.total_mem)
        result["disk_percent"] = from_union([to_float, from_none], self.disk_percent)
        result["cpu_percent"] = from_union([to_float, from_none], self.cpu_percent)
        result["cpu_frequency"] = from_union([to_float, from_none], self.cpu_frequency)
        return result


def data_from_dict(s: Any) -> Data:
    return Data.from_dict(s)


def data_to_dict(x: Data) -> Any:
    return to_class(Data, x)
