import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    role_name = sa.Column(sa.String)
    email = sa.Column(sa.Text, unique=True)
    username = sa.Column(sa.Text, unique=True)
    sex = sa.Column(sa.String)
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
    max_mans = sa.Column(sa.Integer)
    max_womans = sa.Column(sa.Integer)


class GroupMember(Base):
    __tablename__ = 'groups_members'

    id = sa.Column(sa.Integer, primary_key=True)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('groups.id'), nullable=False)
    member_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)


class GroupInstructor(Base):
    __tablename__ = 'groups_instructors'

    id = sa.Column(sa.Integer, primary_key=True)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('groups.id'), nullable=False)
    instructor_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)


class InstructorWorkingHours(Base):
    __tablename__ = 'instructors_workigs_hours'

    id = sa.Column(sa.Integer, primary_key=True)
    instructor_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    min_hours = sa.Column(sa.Integer, nullable=False)
    max_hours = sa.Column(sa.Integer, nullable=False)
    preferred_start = sa.Column(sa.Time)
    preferred_end = sa.Column(sa.Time)
