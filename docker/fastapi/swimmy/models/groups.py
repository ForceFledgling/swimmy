from typing import Optional

from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    description: Optional[str]


class Group(GroupBase):
    id: int
    places: int
    max_mans: int
    max_womans: int

    class Config:
        orm_mode = True


class GroupCreate(GroupBase):
    '''Создал в целях документации и дальнейшего расширения'''
    pass


class GroupUpdate(GroupBase):
    '''Создал в целях документации и дальнейшего расширения'''
    pass


class GroupMemberBase(BaseModel):
    group_id: int
    member_id: int


class GroupMember(GroupMemberBase):
    id: int

    class Config:
        orm_mode = True


class GroupInstructorBase(BaseModel):
    group_id: int
    instructor_id: int


class GroupInstructor(GroupInstructorBase):
    id: int

    class Config:
        orm_mode = True
