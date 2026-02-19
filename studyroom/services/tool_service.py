# services/tag_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from studyroom.models.tool import Tool
from studyroom.schemas.tool import ToolCreate
from studyroom.repositories.tool_repository import tool_repository

class ToolService:
    def create_tool(self, db: Session, data: ToolCreate):
        with db.begin():
            # 1. 이미 존재하는 태그인지 확인
            existing_tag = tool_repository.find_by_name(db, data.name)
            if existing_tag:
                raise HTTPException(status_code=400, detail="이미 존재하는 도구입니다.")

            # 2. 태그 생성 및 저장
            new_tool = Tool(name=data.name)

            tool_repository.save(db, new_tool)

        db.refresh(new_tool)
        return new_tool

    def read_tools(self, db: Session):
        return tool_repository.find_all(db)

tool_service = ToolService()