from core.db import Base

from sqlalchemy import Column, Integer


class Pool(Base):
    '''Модель описывающая бассейны'''

    __tablename__ = 'swimmy_pool'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    lines = Column(Integer)
