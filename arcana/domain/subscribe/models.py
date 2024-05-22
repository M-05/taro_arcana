from sqlalchemy import Column, String, Integer, DateTime, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()


# UTC 시간에서 9시간을 더한 현재 시간을 반환하는 함수
def current_time():
    return datetime.utcnow() + timedelta(hours=9)


#####
# 구독
#####
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    favorite_celebrity = Column(String, nullable=True)
    subscribed_date_and_time = Column(DateTime, default=current_time)
