from pydantic import BaseModel


class BaseUser(BaseModel):
    # role_id: int
    email: str
    username: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'  # bearer - так называют авторизацию на основе access_token
