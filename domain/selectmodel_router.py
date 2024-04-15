from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

# 템플릿 디렉터리 설정
templates = Jinja2Templates(directory="templates")

@router.get('/selectmodel', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("selectmodel.html", {"request": request})