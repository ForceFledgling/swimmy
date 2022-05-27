from core.db import Base

from sqlalchemy import Boolean, Column, DateTime, Integer, String


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    gender = Column(String)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    date = Column(DateTime)
    is_active = Column(Boolean)
    is_administrator = Column(Boolean)
    is_instructor = Column(Boolean)
