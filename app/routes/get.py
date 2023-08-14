from fastapi import APIRouter

from app.db.base import markers
from app.db.drive.images import get_image
from app.lib.excel_sheet_generate import get_spread_sheet

router = APIRouter(
    prefix="/get",
    # tags=["get"]
)


@router.get("/project")
async def project_full_route(project_id: str):
    return markers.get_project_full(project_id)


@router.get("/markers")
async def get_markers_route(project_id: str, level: int, element: str):
    return markers.get_markers(project_id,
                               level,
                               element)


@router.get("/image/{project_id}/{filename}")
async def get_image_route(
    project_id: str,
    filename: str,
):
    return get_image(project_id, filename)


@router.get("/excel")
async def get_spread_sheet_route(project_id: str, level: int, element_id: str):
    return get_spread_sheet(project_id, level, element_id)

