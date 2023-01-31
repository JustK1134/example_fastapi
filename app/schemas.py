from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional






class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass

class UserBase(BaseModel):
    #id: int
    email: EmailStr
    password: str
    #created_at: datetime

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime
    class Config:
        orm_mode=True

class UserCredential(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Post(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    dir: int