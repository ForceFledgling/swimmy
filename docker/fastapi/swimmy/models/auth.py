from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserSex(str, Enum):
    male = 'male'
    female = 'female'


class BaseUser(BaseModel):
    email: str
    username: str
    sex: UserSex


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int
    role_name: Optional[str]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
