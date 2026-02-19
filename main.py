from fastapi import FastAPI

from studyroom import models
from database import engine, Base
from studyroom.routers.user_router import router as user_router
from studyroom.routers.tool_router import router as tool_router
from studyroom.routers.room_router import router as room_router

# 기존 테이블 지우기
# models.Base.metadata.drop_all(bind=engine)

# 정의된 모델들을 기반으로 DB에 테이블을 생성한다.
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(room_router)
app.include_router(tool_router)

@app.get("/")
def read_root():
    return "main fastapi"
