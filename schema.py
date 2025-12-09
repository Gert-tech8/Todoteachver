from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    first_name: str | None = None
    last_name: str | None = None

class User(UserBase):
    id: int
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        orm_mode = True

class Task(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    date: str
    time: str
    completed: bool

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str
    description: str
    owner_id: int
    date: str
    time: str
    completed: Optional[bool] = False

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str]= None
    description: Optional[str] = None
    completed: Optional[bool] = None

