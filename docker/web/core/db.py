import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB = {
    'HOST': os.environ.get("POSTGRES_HOST"),
    'DB': os.environ.get("POSTGRES_DB"),
    'USER': os.environ.get("POSTGRES_USER"),
    'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
}

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB["USER"]}:{DB["PASSWORD"]}@{DB["HOST"]}/{DB["DB"]}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
