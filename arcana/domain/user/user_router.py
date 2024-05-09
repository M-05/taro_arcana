from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from domain.user import database, schema, models, user_crud

from typing import Optional, List
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

router = APIRouter(
                    prefix="/user"
)

# @router.get("/user", response_class=HTMLResponse)
# async def about(request: Request):
#     return templates.TemplateResponse("user.html", {"request": request})


# 게시판 정보 생성 엔드포인트
@router.post("/signup", description="회원가입")
async def signup(
                name: str = Form(...),
                phone: str = Form(...), 
                password: str = Form(...), 
                email: str = Form(...), 
                db: Session = Depends(get_db)
                ):
    """
    회원 가입
    name: str
    phone: str
    password: str
    email: str
    """
    # 이메일 주소로 회원인지 아닌지 확인.
    check_user = user_crud.get_user(email, db)
    if check_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="유저가 존재합니다.")

    new_user = schema.NewUserForm(name=name, phone=phone, password=password, email=email)
    user_crud.create_user(new_user, db)
    return HTTPException(status_code=status.HTTP_200_OK, detail="회원가입 성공")

    


@router.post(path="/login", description="로그인")
async def login(login_form: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user_email = login_form.username
    print("-" * 15)
    print(login_form.username)
    # print(dir(login_form))
    # 'client_id', 'client_secret', 'grant_type', 'password', 'scopes', 'username']
    print("-" * 15)
    check_user = user_crud.get_user(user_email, db)
    print("-" * 15)
    print(check_user)
    print("-" * 15)
    if not check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이름 혹은 비밀번호가 틀립니다.")
    
    #로그인
    result = user_crud.verify_password(login_form.password, check_user.hashed_pw)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이름 혹은 비밀번호가 틀립니다.")
    
    return HTTPException(status_code=status.HTTP_200_OK, detail="로그인 성공")
    
