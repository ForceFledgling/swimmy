from typing import Optional

from pydantic import BaseModel


class Group(BaseModel):
    id: int
    name: str
    desciption: Optional[str]

    class Config:  # указываем что загружаем результат не из питоновских словарей а из моделей ормки
        orm_mode = True
