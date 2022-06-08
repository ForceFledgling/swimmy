from fastapi import APIRouter

from .auth import router as auth_router
from .groups import router as groups_router
from .instuctots import router as instructors_router
from .roles import router as roles_router
from .rooms import router as rooms_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(roles_router)
router.include_router(groups_router)
router.include_router(rooms_router)
router.include_router(instructors_router)
