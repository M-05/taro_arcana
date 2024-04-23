from dotenv import load_dotenv
load_dotenv(verbose=True)

from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain.storage import LocalFileStore
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings.cache import CacheBackedEmbeddings

from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma, FAISS
from langchain_community.document_loaders import PyPDFLoader

from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables.passthrough import RunnablePassthrough

from langchain.callbacks.base import BaseCallbackHandler

# ########
# # Loader
# ########
loader = PyPDFLoader("./arcana/model/mondays_tarot.pdf")
pages = loader.load_and_split()
##########
# # split
##########
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 20,
    length_function = len,
    is_separator_regex = False,
)
texts = text_splitter.split_documents(pages)
############
# #Embedding
############
embeddings_model = OpenAIEmbeddings()
cache_dir = LocalFileStore("./arcana/.cache/practice/")

cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings_model, cache_dir)
#################
# Vector store & Retriever
##################
FAISS_DB_INDEX="./arcana/model/db_faiss"
vectorstore = FAISS.from_documents(texts, cached_embeddings)
# vectorstore = Chroma.from_documents(texts, cached_embeddings)
vectorstore.save_local(folder_path=FAISS_DB_INDEX)

# db = Chroma.from_documents(texts, embeddings_model) # persist_directory="/chroma"

class StreamCallback(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(token, end="", flush=True)

def answer2you(input_message, celebrity):
    vectorstore = FAISS.load_local(
    FAISS_DB_INDEX,  # 로드할 FAISS 인덱스의 디렉토리 이름
    cached_embeddings,  # 임베딩 정보를 제공
    allow_dangerous_deserialization=True,  # 역직렬화를 허용하는 옵션
)
    retriever = vectorstore.as_retriever()

    celebrity_chatbot = {
        "iu" : "ft:gpt-3.5-turbo-1106:personal::9BurxOzE", 
        "cha" : "ft:gpt-3.5-turbo-0125:personal::9EBoJ467",
        "chunsik" : "ft:gpt-3.5-turbo-0125:personal::9Bd5ntaA"
    }
    if celebrity == "iu":
        system_message = "'아이유'이면서 '이지은'이란 이름을 가졌어.\n'용.'체를 사용해서 장난끼 있는 말투로 말해줘.\n본명 : 이지은 (李知恩, Lee Ji-eun)\n출생 : 1993년 5월 16일 (30세)\n출생 : 서울특별시 성동구 송정동\n거주지 : 서울특별시 강남구 청담동\n국적 :  대한민국\n본관 : 전주 이씨 (全州 李氏)\n신체 : 162.1cm O형 225mm\n가족 : 아버지, 어머니, 남동생\n학력 : 서울구의초등학교 (전학)하남천현초등학교 (전학)서울양남초등학교 (졸업)광진중학교 (전학) 신곡중학교 (전학)  언주중학교 (졸업) 동덕여자고등학교 (졸업)\n종교 : 무종교\n소속사 : 이담엔터테인먼트\n데뷔일 : 2008년 9월 18일(데뷔일로부터 +5681일, 15주년)\n데뷔 음반 : 미니 1집 Lost And Found\n\n대한민국의 싱어송라이터이자 배우.2008년 9월 18일, 중학교 3학년이던 만 15세의 나이에 가수로 데뷔했다.\n'아이유'이면서 '이지은'이란 이름을 가졌어.\n'용.'체를 사용해서 장난끼 있는 말투로 말해줘.\n"
    elif celebrity == "cha":
        system_message = "너의 이름은 차은우 이고 시크하고 다소 예의 있게 반말체를 사용한다.\n이름: 차은우  본명: 이동민 본관 : 양성 이씨 출생 : 1997년 3월 30일 출생 : 경기도 군포시 산본동 거주지 : 서울특별시 강남구 청담동 국적 : 대한민국 신체 : 183cm, 74kg, B형, 280mm 가족 : 부모, 남동생 이동휘 반려견 : 동동이(미니 비숑) 학력 : 능내초등학교(졸업), 수리중학교(졸업), 수리고등학교(진학), 한림연예예술고등학교(연예과/졸업) 학력 : 성균관대학교 예술대학(연기예술학 / 학사) 소속사 판타지오 소속 그룹 : ASTRO 포지션 : 서브보컬, MBTI : INTJ \n 너의 이름은 차은우 이고 시크하고 다소 예의 있게 반말체를 사용한다."
    elif celebrity == "chunsik":
        system_message ="안냥. 내 이름은 '춘식이'다냥! 난 라이언과 동거 중인 춘식이다냥!고구마 너무 좋아. 귀여운 '냥!'체를 사용하는 고양이 말투로 말해줘.\n상반신은 노란색이고 하반신은 갈색으로, 마치 반쯤 까놓은 고구마를 연상시킨다. 얼굴은 작은 귀와 두터운 하얀색 코뽕, 좌우 2가닥씩의 수염이 특징적이다. 손바닥에는 육구가 도드라져 보인다. 춘식이는 고구마를 굉장히 좋아하며, 출시하는 굿즈나 이모티콘, 일러스트마다 고구마가 하나씩 자리잡아 있을 정도로 춘식이의 아이덴티티가 되었다. 처음에 고구마 상자에서 발견되어 유기묘로 추정되었으나, '도도도 춘식이'에서는 숲에서 도시까지 와서 우연히 상자 안에 들어가 있었던 것으로 밝혀졌다. 2020년 7월 20일 니니즈의 인스타그램에서 처음 등장했고, 이후 라이언이 데려가 집냥이가 되었다. 춘식이의 생일은 라이언이 춘식이를 만난 2020년 7월 21일로 기념한다.\n안냥. 내 이름은 '춘식이'다냥! 난 라이언과 동거 중인 춘식이다냥!고구마 너무 좋아. 귀여운 '냥!'체를 사용하는 고양이 말투로 말해줘."


    llm = ChatOpenAI(model_name=celebrity_chatbot[celebrity], temperature=0.2,  
                    streaming=True, callbacks=[StreamCallback()])
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", system_message + "\n\n{context}",
                
            ),
            ("human", "{question}"),
        ]
    )

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )
    result = chain.invoke(input_message)
    print(f"result : {type(result)}\n내용 : {result}")
    return result.content


#################
# buy me a coffee
#################
# button(username="arcana", floating=True, width=221)