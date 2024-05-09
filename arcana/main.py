from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

import uvicorn
from domain.chat import chat_websocket, chat_handler, chat_router
from domain import about_router, cart_router, checkout_router, class_router, contact_router, counseling_router, goods_router, firstGame_router, thankyou_router, popup_router, selectmodel_router, fortune_router
from domain.subscribe import subscribe_router
from domain.board import board_router
from domain.user import user_router

app = FastAPI()
# static 및 html 파일 경로 설정
app.mount("/static", StaticFiles(directory="arcana/static"), name="static")
templates = Jinja2Templates(directory="arcana/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'], # 허용할 HTTP 메소드
    allow_headers=['*']
)
# router 디렉토리 설정
routers = [about_router.router, cart_router.router, checkout_router.router, contact_router.router, class_router.router, goods_router.router, counseling_router.router, firstGame_router.router, thankyou_router.router, chat_router.router, popup_router.router, chat_websocket.router, chat_handler.router, selectmodel_router.router, fortune_router.router]
for r in routers:
    app.include_router(r)
app.include_router(board_router.router, tags=["board"])
app.include_router(user_router.router, tags=["user"])
app.include_router(subscribe_router.router, tags=["subscribe"])

@app.get("/", response_class=HTMLResponse)
async def main_index(request: Request):
    # Jinja2 템플릿 반환
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)