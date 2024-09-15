from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    username: str = Field(max_length=100)
    email: str = Field(max_length=100)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserLoginModel(BaseModel):
    email: str = Field(max_length=100)
    password: str = Field(min_length=6)