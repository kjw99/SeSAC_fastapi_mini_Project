# repositories/tag_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from studyroom.models.tool import Tool

class ToolRepository:
    def save(self, db: Session, tool: Tool):
        db.add(tool)
        return tool

    def find_all(self, db: Session):
        # scalars().all()을 사용하여 Tag 객체 리스트를 가져온다.
        return db.scalars(select(Tool)).all()

    async def find_by_name(self, db: AsyncSession, name: str):
        return await db.scalar(select(Tool).where(Tool.name == name))

tool_repository = ToolRepository()