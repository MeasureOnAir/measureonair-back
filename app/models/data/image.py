from pydantic import BaseModel


class ImageDims(BaseModel):
    height: float
    width: float


class ImageData(BaseModel):
    name: str
    dims: ImageDims
