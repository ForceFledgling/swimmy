from typing import Optional

from pydantic import BaseModel


class RoleName(BaseModel):
    administrator = 'administrator'
    instructor = 'instructor'
    client = 'client'


class RoleBase(BaseModel):
    name: Optional[str]


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True  # указываем что загружаем результат не из питоновских словарей а из моделей ормки
