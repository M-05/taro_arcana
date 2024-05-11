import re
from pydantic import BaseModel, Field, validator, constr
from typing import Optional
from datetime import datetime

from fastapi import HTTPException


class NewUserForm(BaseModel):
    # name: constr(min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=10)
    phone: str = Field(..., min_length=1, max_length=13)
    password: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=100)

    @validator('email','name', 'phone', 'password')
    def check_empty(cls, value):
        if not value or value.isspace():
            raise HTTPException(status_code=422, detail="필수 항목을 입력해주세요.")
        return value

    @validator('phone')
    def check_phone(cls, value):
        # value = value.replace("-", "")
        # # 번호 형식 변환: 01012341234 -> 010-1234-1234
        # formatted_phone = f"{value[:3]}-{value[3:7]}-{value[7:]}"
        if '-' not in value or len(value) != 13:
            raise HTTPException(status_code=422, detail="'-'를 포함해서 번호를 입력해주세요.")
        return value



    @validator('password')
    def check_password(cls, value):
        if len(value) < 8:
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함하여 작성해 주세요.")
        
        if not any(char.isdigit() for char in value):
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함하여 작성해 주세요.")
        
        if not any(char.isalpha() for char in value):
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함하여 작성해 주세요.")
        return value
    
    @validator('email')
    def check_email(cls, value):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError('올바른 이메일 형식이 아닙니다.')
        return value