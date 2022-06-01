from enum import Enum

from pydantic import BaseModel


class RoleName(str, Enum):
    administrator = 'administrator'
    instructor = 'instructor'
    client = 'client'


class RoleBase(BaseModel):
    name: RoleName


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True  # указываем что загружаем результат не из питоновских словарей а из моделей ормки
