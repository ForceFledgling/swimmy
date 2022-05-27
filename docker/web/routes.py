from fastapi import APIRouter

from swimmy import pool

from user import user

routes = APIRouter()
routes.include_router(pool.router, prefix='/pool')
routes.include_router(user.router, prefix='/user')