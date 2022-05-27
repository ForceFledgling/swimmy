from pydantic import BaseModel


class PoolBase(BaseModel):
    lines: int

    class Config:
        orm_mode = True


class PoolList(PoolBase):
    id: int


class PoolCreate(PoolBase):
    pass
