from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

router = APIRouter()
templates = Jinja2Templates(directory="arcana/templates")

# class celebInput(BaseModel):
#     celebName: str

@router.get('/firstGame')
async def first_game(request: Request):
    
    # print(f"model : \n{model}")
    # if not model:
    #     raise HTTPException(status_code=400, detail="Celebrity name is required.")
    
    # if model not in ['iu', 'cha', 'chunsik']:
    #     raise HTTPException(status_code=404, detail="Celebrity not found.")
    

    return templates.TemplateResponse("firstGame.html", {"request": request})