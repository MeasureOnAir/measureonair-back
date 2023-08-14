from typing import List, Union, Dict
from pydantic import BaseModel

from app.models.data.image import ImageData
from app.models.request.project import ElementEnum, MarkerObj


class Element(BaseModel):
    id: str = ""
    name: str = ""
    image: Union[ImageData, None] = None
    markers: Union[Dict[str, MarkerObj], None] = {}


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
