from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostDef(BaseModel):
    title: str
    content: str
    published: bool=True

class CreatePost(PostDef):
    pass

class User(BaseModel): #info. from user is a Pydantic model object.
    email: EmailStr
    password: str

class RespToUser(BaseModel): #response from Orm is an ORM model Instance(Specific User).
    id: int
    email: EmailStr
    created_at: datetime

    class Config: #Converts ORM model Instance into Pydantic model Instance.
        orm_mode = True

class Response(PostDef): #reflected in postman, shows all public posts with owner info.
    id: int
    created_at: datetime
    user_id: int
    owner: RespToUser

    class Config:
        orm_mode = True

class RespAfterVotes(BaseModel):
    Posts: Response
    votes: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: bool
    