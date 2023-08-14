from typing import List

from fastapi import APIRouter
from app.db.base import users
from app.models.data.users import UserShort, UserFull

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/all")
async def route_user_all():
    return users.get_users()


@router.get("/get")
async def route_user_get(user_id: str):
    return users.get_user(user_id)


@router.post("/add")
async def route_user_add(user: UserShort):
    _new_user = users.add_user(user)
    return _new_user


@router.put("/update")
async def route_user_update(user: UserFull):
    _updated_user = users.update_user(user)
    return _updated_user


@router.delete("/remove")
async def route_user_remove(user_key: str):
    _removed_user = users.remove_user(user_key)
    return _removed_user


@router.post("/project/add")
async def route_user_project_add(user_id: str, project_id: str):
    return users.add_project(user_id, project_id)


@router.delete("/project/remove")
async def route_user_project_remove(user_id: str, project_id: str):
    return users.remove_project(user_id, project_id)
