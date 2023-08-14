from enum import Enum
from typing import Union
from pydantic import BaseModel


class TypeEnum(str, Enum):
    MT1 = "point"
    MT2 = "line"
    MT3 = "area"


class Location(BaseModel):
    x: float = 0.0
    y: float = 0.0


class Marker(BaseModel):
    id: str
    type: TypeEnum
    # location: Location = None
    length: float = 1.0
    width: float = 1.0
    height: float = 1.0
    qty: float = 1.0
    times: int = 1
    unit: str = "meter"
    remarks: Union[str, None] = ""
