from fastapi import APIRouter

from app.db.base import meta

router = APIRouter(
    prefix="/all",
    # tags=["all"]
)


@router.get("/project")
async def all_project(user_id: str):
    _projects = meta.get_project_all(user_id)
    if _projects:
        return _projects, 200
    else:
        return "No Projects Found For the User", 404
