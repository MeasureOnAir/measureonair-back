from typing import List, Union, Dict
from pydantic import BaseModel
from enum import Enum

from app.modals.data.image import ImageData
from app.modals.data.marker import Marker


class MarkerReq(BaseModel):
    project_id: str
    level: int
    element: str
    markers: Dict[str, Marker] = []


class ElementEnum(str, Enum):
    EL001 = "floor"
    EL002 = "wall"
    EL003 = "door"
    EL004 = "window"
    EL005 = "paint"
    EL006 = "roof"


class Element(BaseModel):
    element: ElementEnum
    image: Union[ImageData, None] = None
    markers: List[Marker] = []


class Level(BaseModel):
    num: int = 0
    elements: List[Element] = []


class Project(BaseModel):
    name: str = ""
    description: str = ""
    num_levels: int = 0
    elements: List[str] = []
