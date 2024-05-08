from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import and_

from domain.board.models import Board
from domain.board import schema
from domain.board import database



def insert_post(new_post: schema.NewPost,
                db: Session):
    post = Board(
        writer = new_post.writer,
        title = new_post.title,
        content = new_post.content,
        del_yn = new_post.del_yn
    )

    db.add(post)
    db.commit()

    return post.no

def list_all_post(db: Session):
    lists = db.query(Board).filter(Board.del_yn == 'Y').all()
    print(lists)
    return [schema.PostList(no=row.no,
                    writer=row.writer,
                    title=row.title,
                    date=row.date) for row in lists]

def get_post(post_no: int, db: Session):
    try:
        print(db.query(Board))
#         SELECT board.no AS board_no, board.writer AS board_writer, board.title AS board_title, board.content AS board_content, board.date AS board_date, board.del_yn AS board_del_yn 
#         FROM board
        post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
        print(post)
        # <domain.board.models.Board object at 0x12e031e40>

        return schema.Post(no=post.no,
                    writer=post.writer,
                    title=post.title,
                    content=post.content,
                    date=post.date)
    except Exception as e:
        return {"error": str(e), "msg": "존재하지 않는 게시글 번호입니다."}
    
def update_post(update_post: schema.UpdatePost, db: Session):
    post = db.query(Board).filter(and_(Board.no == update_post.no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는 게시글 번호입니다.")
        
        post.title = update_post.title
        post.content = update_post.content
        db.commit()
        db.refresh(post)
        return get_post(post.no, db)
    except Exception as e:
        return str(e)
    

def alter_del_yn(post_no: int, db: Session):
    post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는 게시글 번호입니다.")
        
        post.del_yn = "N"
        db.commit()
        db.refresh(post)
        return {"msg" : "게시글 숨기기가 완료되었습니다."}
    
    except Exception as e:
        return str(e)
    
def delete_post(post_no: int, db: Session):
    post = db.query(Board).filter(and_(Board.no == post_no, Board.del_yn == "Y")).first()
    try:
        if not post:
            raise Exception("존재하지 않는 게시글 번호입니다.")
        
        db.delete(post)
        db.commit()
        db.refresh(post)
        return {"msg" : "삭제가 완료되었습니다."}
    
    except Exception as e:
        return str(e)