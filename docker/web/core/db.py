import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB = {
    'HOST': os.environ.get("POSTGRES_HOST"),
    'NAME': os.environ.get("POSTGRES_NAME"),
    'USER': os.environ.get("POSTGRES_USER"),
    'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
}

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB["USER"]}:{DB["PASSWORD"]}@{DB["HOST"]}/{DB["NAME"]}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
