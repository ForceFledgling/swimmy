from core.utils import get_db

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from . import service
from .schemas import PoolCreate

router = APIRouter()


@router.get('/')
def pool_list(db: Session = Depends(get_db)):
    return service.get_pool_list(db)


@router.post('/')
def pool_create(item: PoolCreate, db: Session = Depends(get_db)):
    return service.create_pool(db, item)
