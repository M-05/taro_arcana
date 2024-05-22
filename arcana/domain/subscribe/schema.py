import re
from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional


class SubscriptionCreate(BaseModel):
    name: constr(min_length=1, max_length=50)  # 최소 1자 이상, 최대 50자 이하여야 함
    email: EmailStr
    age: constr(max_length=10)
    gender: constr(pattern=r'^[남여]$')  # 선택 사항이므로 추가적인 유효성 검사 규칙이 없음
    favorite_celebrity: Optional[str] = None

    @validator('name')
    def check_name(cls, value):
        if len(value) == 0:
            raise ValueError("1글자 이상 작성 해주세요.")
        return value

    @validator('age')
    def check_age(cls, value):
        valid_ages = ['10대 미만', '20대', '30대', '40대', '50대 이상']
        if value not in valid_ages:  # 유효한 나이 범위인지 확인
            raise ValueError('유효한 나이를 선택해주세요.')
        return value
        # if not value.endswith('대'):

    @validator('gender')
    def check_gender(cls, value):
        if value not in ["남", "여"]:
            raise ValueError('성별은 "남" 또는 "여"여야 합니다.')
        return value

    @validator('email')
    def check_email(cls, value):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError('올바른 이메일 형식이 아닙니다.')
        return value
