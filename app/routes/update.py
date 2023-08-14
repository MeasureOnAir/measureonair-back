from fastapi import APIRouter

from app.db.base import markers

router = APIRouter(
    prefix="/update",
    # tags=["update"]
)


@router.get("/project")
async def all_project():
    _markers = markers.get_base()
    _markers.insert({
        "key": "abc100",
        "name": "Geordi",
        "title": "Chief Engineer"
    })

    fetch_res = _markers.fetch({"name": "Geordi"})

    # return ["MOA-1", "MOA-2"]
    return fetch_res


# users.insert({
#     "name": "Geordi",
#     "title": "Chief Engineer"
# })
#
# fetch_res = users.fetch({"name": "Geordi"})
#
# for item in fetch_res.items:
#     users.delete(item["key"])