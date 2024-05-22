from fastapi import APIRouter
from model import model_chat
from pydantic import BaseModel
import json

router = APIRouter()


# 카드 정보를 받기 위한 Pydantic 모델
class CardInfo(BaseModel):
    cardPath: str


# route_handler.py
# 카드 정보를 받는 엔드포인트
@router.post("/cardPath")
async def receive_card_info(card_info: CardInfo):
    # 카드 정보 처리
    # 예: 데이터베이스에 저장, 로그 출력 등
    print(f"Received card info: \n{card_info.cardPath}")
    data = {"imgPath": card_info.cardPath}
    json_data = json.dumps(data)
    # JSON 데이터를 파일에 저장
    with open("./arcana//static/imgPath.json", "w") as f:
        f.write(json_data)
    # client_id = "arcana"
    return {"message": "Card info received successfully"}


class celebInfo(BaseModel):
    celebText: str


# route_handler.py
@router.post("/celebName")
async def receive_celeb_info(celeb_info: celebInfo):
    # 카드 정보 처리
    # 예: 데이터베이스에 저장, 로그 출력 등
    print(f"Received celeb info: \n{celeb_info.celebText}")
    data = {"celebName": celeb_info.celebText}
    json_data = json.dumps(data)
    # JSON 데이터를 파일에 저장
    with open("./arcana//static/celebName.json", "w") as f:
        f.write(json_data)
    # client_id = "arcana"
    return {"message": "celeb info received successfully"}
