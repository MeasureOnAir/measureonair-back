from typing import List, Union, Dict
from pydantic import BaseModel

from app.modals.data.image import ImageData
from app.modals.data.marker import Marker
from app.modals.request.project import ElementEnum


class Element(BaseModel):
    id: str = ""
    name: str = ""
    image: Union[ImageData, None] = None
    markers: Dict[str, Marker] = {}


class Level(BaseModel):
    num: int = 0
    elements: Dict[str, Element] = {}


class ProjectMeta(BaseModel):
    id: str = ""
    name: str = ""
    description: str = ""
    num_levels: int = 0
    elements: List[ElementEnum] = []


class ProjectFull(BaseModel):
    project_id: str
    project_meta: ProjectMeta
    levels: Dict[int, Level] = {}
