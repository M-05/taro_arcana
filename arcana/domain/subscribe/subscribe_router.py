from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import domain.subscribe.database as database
from domain.subscribe.schema import SubscriptionCreate
import domain.subscribe.models as models

from typing import Optional
from starlette import status

templates = Jinja2Templates(directory="arcana/templates")


engine = database.engineconnect()
session = engine.sessionmaker()

def get_db():    
    try:
        yield session
    finally:
        # pass
        session.close()

router = APIRouter()

@router.get("/popup", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("popup.html", {"request": request})


# 구독 정보 생성 엔드포인트
@router.post("/popup")
async def create_subscription(  
                                name: str = Form(...),
                                email: str = Form(...), 
                                age: str = Form(...), 
                                gender: str = Form(...), 
                                favorite_celebrity: Optional[str] = Form(None), 
                                db: Session = Depends(get_db)):
    """
    구독
    """
    try:
        subscription_data = SubscriptionCreate(name=name,
                                                email=email, 
                                                age=age, 
                                                gender=gender, 
                                                favorite_celebrity=favorite_celebrity)
        db_subscription = models.Subscription(**subscription_data.dict())
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
    
        return JSONResponse(content={"message": "구독이 완료되었습니다!", "name": name, "email": email})
        
    except IntegrityError as e:
        db.rollback()
        return JSONResponse(status_code=400, content={"message": "이미 해당 이메일 주소가 등록되어 있습니다."})
        
    except Exception as e:
        db.rollback()
        # return {"제대로 입력하세요"}
        return JSONResponse(status_code=500, content={"message": "서버에서 오류가 발생했습니다. 문제를 해결할 수 없습니다."})
        

# 모든 구독 정보 확인.
###########
# 인코딩 문제.
###########
# @router.get("/subscriptions")
# async def read_subscriptions(db: Session = Depends(get_db)):
#     return session.query(models.Subscription).all()