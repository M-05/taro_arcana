import logging
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

import uvicorn
from domain.chat import chat_websocket, chat_handler, chat_router
from domain import (about_router, cart_router, checkout_router, class_router,
                    contact_router, counseling_router, goods_router,
                    firstGame_router, thankyou_router, popup_router,
                    selectmodel_router, fortune_router)
from domain.subscribe import subscribe_router
from domain.board import board_router
from domain.user import user_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
    )
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.debug(f"Debug: Request received at {request.url}")
        logger.info(f"Request: {request.method} {request.url}")
        try:
            response: Response = await call_next(request)
            print(call_next(request))
            logger.info(f"Request: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Error: Exception occurred - {str(e)}")
            raise e
        finally:
            logger.debug(f"Debug: Completed processing request at {request.url}")


app = FastAPI()
# static 및 html 파일 경로 설정
app.mount("/static", StaticFiles(directory="arcana/static"), name="static")
templates = Jinja2Templates(directory="arcana/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],  # 허용할 HTTP 메소드
    allow_headers=['*']
)
app.add_middleware(LoggingMiddleware)

# router 디렉토리 설정
routers = [
    about_router.router, cart_router.router, checkout_router.router,
    contact_router.router, class_router.router, goods_router.router,
    counseling_router.router, firstGame_router.router, thankyou_router.router,
    chat_router.router, popup_router.router, chat_websocket.router,
    chat_handler.router, selectmodel_router.router, fortune_router.router
]
for r in routers:
    app.include_router(r, tags=["web"])

app.include_router(board_router.router, tags=["board"])
app.include_router(user_router.router, tags=["user"])
app.include_router(subscribe_router.router, tags=["subscribe"])


@app.get("/", response_class=HTMLResponse)
async def main_index(request: Request):
    # Jinja2 템플릿 반환
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
