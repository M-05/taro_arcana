from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# router = APIRouter(prefix='/about') -> /about/about 주소로.
router = APIRouter()

# 템플릿 디렉터리 설정
templates = Jinja2Templates(directory="arcana/templates")


@router.get('/popup', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("popup.html", {"request": request})
