from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from model import model_chat
from pydantic import BaseModel
import json

router = APIRouter()

# def load_celebName():
#     import json

#     with open("./arcana//static/celebName.json", "r") as f:
#         celebName = json.loads(f.read())
#         # print(type(celebName))
#         if celebName['celebName'] == 'iu':
#             return 0
#         elif celebName['celebName'] == 'cha':
#             return 1
#         else:
#             return 2


@router.websocket('/chatting')
async def websocket_chatting(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            print(data)
            message = data["message"]
            time = data.get("time", "")  # 클라이언트에서 보낸 시간 정보를 가져옵니다.
            sender = data.get("sender", "나")  # 클라이언트에서 보낸 발신자 정보를 가져옵니다.
            celebName = data['celebrity']
            print(f"{sender}의 질문 : {message}")
            await websocket.send_json({
                "message": message,
                "sender": "나",
                "time": time
                })

            # 모델을 사용하여 챗봇 응답 생성
            # celebrity = ["iu", "cha", "chun"]

            # reply = model_chat.answer2you(
            #     message,
            #     celebrity[load_celebName()]
            #     )

            # print(f"챗봇의 대답 : {reply}")

            # 클라이언트로 사용자의 메시지와 챗봇의 응답을 전송

            await websocket.send_json({
                "message": model_chat.answer2you(message, celebName),
                "sender": celebName,
                "time": time
                })

    except WebSocketDisconnect:
        print("webSocket dissconnet 입니다.")

########################
# 연예인 클릭하면 그 정보 저장한다.
# celebrity[0] 수정해야한다.
#########################
# 1. 타로 카드 클릭하면 그 정보 저장해야한다.
# -- 음성이 나온다. 나온 후 다음 페이지로.
# 2. 챗봇 페이지로 이동한다.
# 3. 카드 이미지가 채팅 창에 왼쪽에 출력이 된다.
# 3. 해당 타로 이미지에 관련된 질문이 먼저 트리거가 발동한다.
# 4. 그 질문이 챗봇이 대답을 한다.
#########################

# sender 정보
# 카드 정보


# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from pydantic import BaseModel
# from typing import List
# from model import model_chat

# import json


# router = APIRouter()

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     async def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#    async def send_personal_message(
#            self,
#            message: str,
#            websocket: WebSocket
#            ):
#         await websocket.send_json(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_json(message)


# manager = ConnectionManager()

# class CardInfo(BaseModel):
#     cardPath: str

# @router.post("/card-path")
# async def receive_card_info(card_info: CardInfo):
#     print(f"Received card 경로 \n{card_info.cardPath}")

#     data = {"imgPath" : card_info.cardPath}
#     json_data = json.dumps(data)
#     # JSON 데이터를 파일에 저장
#     with open("./static/imgPath.json", "w") as f:
#         f.write(json_data)

    # await manager.broadcast({
    #     "message": card_info.cardPath,
    #     "sender": "시스템",
    #     "time": ""
    #     })
#     return CardInfo(cardPath=card_info.cardPath)


# @router.websocket('/chatting')
# async def websocket_chatting(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_json()  # JSON 형태로 메시지 받기
#             print(f"JS to PY data : {data}")
#             message = data["message"]
#             time = data.get("time", "")
#             sender = data.get("sender", "나")
#        #    print(
#        #        f"data : \nmsg : {message}\ntime : "
#        #        f"{time}\nsender : {sender}"
#        #        )

#             print(f"{sender}의 질문 : {message}")
#            await manager.send_personal_message({
#                "message": message,
#                "sender": "나",
#                "time": time
#                },
#                websocket
#                )

#             celebrity = ["아이유", "차은우", "춘식이"]
#             reply = model_chat.answer2you(message, celebrity[0])

#            # await manager.send_personal_message({
#            #     "message": reply, "sender": celebrity[0], "time": time
#            #     },
#            #     websocket
#            #     )

#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         print("WebSocket disconnected")
