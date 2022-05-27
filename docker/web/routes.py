from fastapi import APIRouter

from swimmy import pool


routes = APIRouter()
routes.include_router(pool.router, prefix='/pool')
