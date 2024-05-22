from sqlalchemy import Column, String, Integer, DateTime, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()


# UTC 시간에서 9시간을 더한 현재 시간을 반환하는 함수
def current_time():
    return datetime.utcnow() + timedelta(hours=9)


######
# 게시판
######
class Board(Base):
    __tablename__ = "board"

    no = Column(Integer, primary_key=True, autoincrement=True)
    writer = Column(VARCHAR(30), nullable=False)
    title = Column(VARCHAR(30), nullable=False)
    content = Column(VARCHAR(100), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    del_yn = Column(VARCHAR(1), nullable=False, default='Y')
