from sqlalchemy import Column, String, Integer, DateTime, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()

# UTC 시간에서 9시간을 더한 현재 시간을 반환하는 함수
def current_time():
    return datetime.utcnow() + timedelta(hours=9)

######
# 유저.
######
class User(Base):
    __tablename__="Users"

    user_no = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(VARCHAR(10), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    phone = Column(VARCHAR(13), nullable=False, unique=True)
    hashed_pw = Column(VARCHAR(100), nullable=False)
    role = Column(VARCHAR(20), nullable=False, default="MEMBER")
    status = Column(VARCHAR(1), nullable=False, default="1")
    regdate = Column(DateTime, nullable=False, default=datetime.now)