from typing import List, Union, Dict
from pydantic import BaseModel
from enum import Enum

from app.models.data.image import ImageData
from app.models.data.marker import Marker


class Size(BaseModel):
    height: Union[float, None]
    width: Union[float, None]


class Coordinates(BaseModel):
    xC: Union[float, None]
    yC: Union[float, None]


class FigureObj(BaseModel):
    id: str
    type: str
    size: Size
    fill: Union[str, None]
    stroke: Union[str, None]
    strokeWidth: Union[float, None]
    position: List[Coordinates]
    viewPort: Size


class MarkerObj(BaseModel):
    data: Marker
    figure: FigureObj


class MarkerReq(BaseModel):
    project_id: str
    level: int
    element: str
    markers: Dict[str, MarkerObj] = {}


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
