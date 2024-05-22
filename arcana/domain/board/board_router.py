from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

import domain.board.database as database
from domain.board import board_crud
from domain.board import schema
import domain.board.models as models

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
                    prefix="/board"
)

# @router.get("/board", response_class=HTMLResponse)
# async def about(request: Request):
#     return templates.TemplateResponse("board.html", {"request": request})


# 게시판 정보 생성 엔드포인트
@router.post("/create", description="게시판 글 쓰기")
async def create_board(
                        writer: str = Form(...),
                        title: str = Form(...),
                        content: str = Form(...),
                        del_yn: str = Form("Y"),
                        db: Session = Depends(get_db)
                        ):
    """
    게시판
    writer: str
    title: str
    content: str
    del_yn: str
    """
    try:
        new_post = schema.NewPost(
            writer=writer,
            title=title,
            content=content,
            del_yn=del_yn
            )
        return board_crud.insert_post(new_post, db)

    except ValueError as ve:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={"message": f"잘못된 요청입니다: {str(ve)}"}
            )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": f"서버에서 오류가 발생했습니다 {str(e)}. 문제를 해결할 수 없습니다."}
                            )


@router.get(
        path="/read",
        description="게시판 조회",
        response_model=List[schema.PostList]
            )
async def read_all_post(db: Session = Depends(get_db)):
    return board_crud.list_all_post(db)


@router.get(
        path="/read/{post_no}",
        description="게시판 상세 조회",
        response_model=schema.Post
        )
async def read_post(
    post_no: int,
    db: Session = Depends(get_db)
                    ):
    return board_crud.get_post(post_no, db)


@router.put(path="/update/{post_no}", description="게시글 수정")
async def update_post(
                    no: int = Form(...),
                    title: str = Form(...),
                    content: Optional[str] = Form(None),
                    db: Session = Depends(get_db)
                    ):

    update_post = schema.UpdatePost(no=no, title=title, content=content)
    return board_crud.update_post(update_post, db)


@router.patch(path="/delete/{post_no}", description="게시글 숨기기")
async def delete_post_yn(
    post_no: int,
    db: Session = Depends(get_db)
                        ):
    return board_crud.alter_del_yn(post_no, db)


@router.delete(path="/delete/{post_no}", description="게시글 삭제")
async def delete_post(
    post_no: int,
    db: Session = Depends(get_db)
                    ):
    return board_crud.delete_post(post_no, db)
