import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    role_name = sa.Column(sa.String)
    email = sa.Column(sa.Text, unique=True)
    username = sa.Column(sa.Text, unique=True)
    password_hash = sa.Column(sa.Text)


class Room(Base):
    __tablename__ = 'rooms'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    sex = sa.Column(sa.String)
    capacity = sa.Column(sa.Integer)


class Group(Base):
    __tablename__ = 'groups'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    description = sa.Column(sa.String, nullable=True)
    places = sa.Column(sa.Integer)
    free_places = sa.Column(sa.Integer)
    max_mans = sa.Column(sa.Integer)
    max_womans = sa.Column(sa.Integer)


class GroupMember(Base):
    __tablename__ = 'groups_members'

    id = sa.Column(sa.Integer, primary_key=True)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('groups.id'), nullable=False)
    member_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
