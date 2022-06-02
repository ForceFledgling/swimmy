from enum import Enum

from pydantic import BaseModel


class RoomSex(str, Enum):
    male = 'male'
    female = 'female'


class RoomBase(BaseModel):
    name: str
    sex: RoomSex
    capacity: int


class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True


class RoomCreate(RoomBase):
    '''Создал в целях документации и дальнейшего расширения'''
    pass


class RoomUpdate(RoomBase):
    '''Создал в целях документации и дальнейшего расширения'''
    pass
