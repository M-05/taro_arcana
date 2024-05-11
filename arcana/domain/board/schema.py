import re
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime



class NewPost(BaseModel):
    writer: str = Field(..., min_length=1, max_length=10)
    title: str = Field(..., min_length=1, max_length=30)
    content: str = Field(..., min_length=1, max_length=1000)
    del_yn: str = Field(..., pattern='^[YyNn]$')

    @validator('writer')
    def check_writer(cls, value):
        if len(value) == 0:
            raise ValueError("이름을 작성해주세요.")
        return value

    @validator('title')
    def check_title(cls, value):
        if len(value) < 1:
            raise ValueError('제목을 적어주세요.')
        return value
    
    @validator('content')
    def check_content(cls, value):
        if len(value) < 1:
            raise ValueError('글을 적어주세요.')
        return value
    
    @validator('del_yn')
    def check_del_yn(cls, value):
        if value not in ["Y", "N", "y", "n"]:
            raise ValueError('"Y" 또는 "N"이여야 합니다.')
        return value.upper()

class PostList(BaseModel):
    no: int
    writer: str
    title: str
    date: datetime

class Post(BaseModel):
    no: int
    writer: str
    title: str
    content: str # Optional[str] = None
    date: datetime

class UpdatePost(BaseModel):
    no: int
    title: str
    content: Optional[str] = None