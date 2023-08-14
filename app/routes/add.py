import uuid
from io import BytesIO
from typing import Dict

from PIL import Image
from fastapi import APIRouter, Body, UploadFile, File
from pdf2image import convert_from_bytes

from app.core.handler_image import resize_image
from app.db.base.markers import add_project_full, add_markers, get_base
from app.db.base.meta import add_project_meta
from app.db.base.users import add_project
from app.db.drive.images import get_drive
from app.models.data.project import ProjectMeta, ProjectFull, Level, Element
from app.models.request.project import Project as ProjectReq, MarkerReq

IMAGE_FORMATS = ["png", "jpg", "jpeg", "pdf"]
router = APIRouter(
    prefix="/add",
    # tags=["add"]
)


@router.post("/project")
async def add_project_route(user_id: str, project_req: ProjectReq = Body(
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
    for level in range(1, project_meta.num_levels+1):
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

    # Add Project to the User
    add_project(user_id, project_id)

    return f"Successfully Created the Project {project_meta.name}, " \
           f"Project Id: {project_id}"


# @router.post("/markers")
# async def add_markers_route(marker_req: MarkerReq = Body(
#     examples={
#         "normal": {
#             "summary": "A normal example",
#             "description": "A **normal** item works correctly.",
#             "value": {
#                 "project_id": "7059bd5e",
#                 "level": 1,
#                 "element": "EL001",
#                 "markers": {"M1":
#                     {
#                         "data": {
#                             "id": "M1",
#                             "type": "point",
#                             "location": {"x": 150, "y": 100},
#                             "length": 1.0,
#                             "width": 1.0,
#                             "height": 1.0,
#                             "times": 1,
#                             "unit": "meter",
#                             "remarks": "Marker Remarks"
#                         },
#                         "image": str
#                     }
#                 }
#             }
#         }
#     }
# )):
@router.post("/markers")
async def add_markers_route(marker_req: MarkerReq):
    add_markers(marker_req.project_id,
                marker_req.level,
                marker_req.element,
                marker_req.markers)
    return "Successfully Added The Markers"


@router.post("/image/")
async def create_upload_file(
        file: UploadFile = File(...),
        project_id: str = "",
        level: int = 1,
        element: str = "",
        page_number: int = 1
):
    file_extension = file.filename.split('.')[-1]
    if file_extension in IMAGE_FORMATS:
        contents = await file.read()
        # Convert PDF to Image
        if file_extension == "pdf":
            images = convert_from_bytes(contents, first_page=page_number, last_page=page_number)
            if len(images) == 0:
                return f"Please Upload a PDF with more than {page_number} pages", 500
            image = images[page_number-1]
            file_extension = "png"
        else:
            image = Image.open(BytesIO(contents))
        width, height = image.size

        # Resize the image
        image = resize_image(image)

        # drive = deta.Drive(f"images/{project_id}/{level}/{element}")
        drive = get_drive(project_id)
        filename = f"{level}-{element}.{file_extension}"
        img_bytes = BytesIO()
        image.save(img_bytes, format=file_extension)
        drive.put(filename, img_bytes.getvalue())
        # drive.put(filename, BytesIO(contents))

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
