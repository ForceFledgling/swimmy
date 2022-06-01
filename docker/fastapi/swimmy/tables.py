import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()  # базовый класс от которого будет всё наследоваться


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    role_name = sa.Column(sa.String)  # sa.ForeignKey('roles.name')
    email = sa.Column(sa.Text, unique=True)
    username = sa.Column(sa.Text, unique=True)
    password_hash = sa.Column(sa.Text)


# class Role(Base):
#     __tablename__ = 'roles'

#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.String, unique=True)


class Group(Base):
    __tablename__ = 'groups'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    description = sa.Column(sa.String, nullable=True)
