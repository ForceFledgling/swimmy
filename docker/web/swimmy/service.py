from sqlalchemy.orm import Session

from .models import Pool
from .schemas import PoolCreate


def get_pool_list(db: Session):
    return db.query(Pool).all()


def create_pool(db: Session, item: PoolCreate):
    pool = Pool(**item.dict())
    db.add(pool)
    db.commit()
    db.refresh(pool)
    return pool
