from fastapi import APIRouter

from .groups import router as groups_router


router = APIRouter()
router.include_router(groups_router)
