from typing import Optional

from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    description: Optional[str]


class Group(GroupBase):
    id: int

    class Config:
        orm_mode = True  # указываем что загружаем результат не из питоновских словарей а из моделей ормки


class GroupCreate(GroupBase):
    '''Создал в целях документации и дальнейшего расширения'''
    pass


class GroupUpdate(GroupBase):
    '''Создал в целях документации и дальнейшего расширения'''
    pass
