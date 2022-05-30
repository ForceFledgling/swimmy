import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()  # базовый класс от которого будет всё наследоваться


class Group(Base):
    __tablename__ = 'groups'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    description = sa.Column(sa.String, nullable=True)
