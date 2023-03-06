import uuid
from io import BytesIO
from typing import Dict

from PIL import Image
from fastapi import APIRouter, Body, UploadFile, File

from app.db.base.markers import add_project_full, add_markers, get_base
from app.db.base.meta import add_project_meta
from app.db.drive.images import get_drive
from app.modals.data.project import ProjectMeta, ProjectFull, Level, Element
from app.modals.request.project import Project as ProjectReq, MarkerReq

IMAGE_FORMATS = ["png", "jpg"]
router = APIRouter(
    prefix="/add",
    # tags=["add"]
)


@router.post("/project")
async def add_project_route(project_req: ProjectReq = Body(
    examples={
        "normal": {
            "summary": "A normal example",
            "description": "A **normal** item works correctly.",
            "value": {
                "name": "Test Project 1",
                "description": "This is a Test Project",
                "num_levels": 5,
                "elements": ["floor", "wall", "door"]
            }
        }
    }
)):
    project_id: str = str(uuid.uuid1()).split("-")[0]
    project_meta: ProjectMeta = ProjectMeta(**{"id": project_id, **project_req.dict()})

    # Create Full Project
    levels: Dict[int, Level] = {}
    for level in range(0, project_meta.num_levels):
        elements: Dict[str, Element] = {}
        for element in project_meta.elements:
            element_obj = Element(id=element.name,
                                  name=element.value,
                                  image=None,
                                  markers=[])
            elements[element.name] = element_obj
        levels[level] = Level(num=level, elements=elements)

    project_full = ProjectFull(project_id=project_id,
                               project_meta=project_meta,
                               levels=levels
                               )

    # Add to the Base
    add_project_meta(project_meta)
    add_project_full(project_full)

    return f"Successfully Created the Project {project_meta.name}, " \
           f"Project Id: {project_id}"


@router.post("/markers")
async def add_markers_route(marker_req: MarkerReq = Body(
    examples={
        "normal": {
            "summary": "A normal example",
            "description": "A **normal** item works correctly.",
            "value": {
                "project_id": "7059bd5e",
                "level": 1,
                "element": "EL001",
                "markers": {"M1":
                    {
                        "id": "M1",
                        "type": "point",
                        "location": {"x": 150, "y": 100},
                        "length": 1.0,
                        "width": 1.0,
                        "height": 1.0,
                        "times": 1,
                        "unit": "meter",
                        "remarks": "Marker Remarks"
                    }
                }
            }
        }
    }
)):
    add_markers(marker_req.project_id,
                marker_req.level,
                marker_req.element,
                marker_req.markers)

    return "Successfully Added The Markers"


@router.post("/image/")
async def create_upload_file(
        file: UploadFile = File(...),
        project_id: str = "",
        level: str = "",
        element: str = "",
):
    file_extension = file.filename.split('.')[-1]
    if file_extension in IMAGE_FORMATS:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        width, height = image.size

        # drive = deta.Drive(f"images/{project_id}/{level}/{element}")
        drive = get_drive(project_id)
        filename = f"{level}-{element}.{file_extension}"
        drive.put(filename, BytesIO(contents))

        # Update Project Database
        db = get_base()
        project_full = db.fetch({'project_id': project_id}).items[0]
        updates = {
            f"levels.{level}.elements.{element}.image":
                {'name': filename, 'dims': {'height': height, 'width': width}}
        }
        db.update(updates, project_full['key'])

        return {
            "filename": filename,
            "width": width,
            "height": height
        }
    else:
        return f"Please Upload A Supported Format. Supported Formats {IMAGE_FORMATS}", 500
