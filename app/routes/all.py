from fastapi import APIRouter

from app.db.base import meta

router = APIRouter(
    prefix="/all",
    # tags=["all"]
)


@router.get("/project")
async def all_project():
    _projects = meta.get_project_all()
    return _projects
