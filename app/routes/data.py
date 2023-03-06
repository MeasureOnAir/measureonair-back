from fastapi import APIRouter

from app.routes import get, all, add, update

router = APIRouter(
    prefix="/data",
    tags=["data"]
)
router.include_router(get.router)
router.include_router(all.router)
router.include_router(add.router)
router.include_router(update.router)
