from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from studyroom.repositories.room_repository import room_repository
from studyroom.repositories.tool_repository import tool_repository
from studyroom.models.room import Room
from studyroom.models.tool import Tool
from studyroom.models.room_tool import RoomTool
from studyroom.schemas.room import RoomCreate
from studyroom.models.user import User


class RoomService:
    async def create_room(self, db: AsyncSession, data: RoomCreate, current_user: User):

        if current_user.user_id != 1:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "관리자 권한이 없습니다."
            )

        new_room = Room(
            name=data.name,
            max_people=data.max_people,
            location=data.location
        )

        async with db.begin():
            for name in data.tools:
                tool = await tool_repository.find_by_name(db, name)

                if not tool:
                    tool = Tool(name=name)
                    tool_repository.save(db, tool)
                    await db.flush()  

                rooms_tools_link = RoomTool(tool=tool)
                new_room.rooms_tools.append(rooms_tools_link)
                
            room_repository.save(db, new_room)
            await db.flush()

        new_room = await room_repository.find_by_id_with_tools(db, new_room.room_id)
        return new_room
    
    def read_rooms(self, db: Session):
        return room_repository.find_all_with_tools(db)

    async def read_room_by_id(self, db: AsyncSession, room_id: int):
        room = await room_repository.find_by_id(db, room_id)
        if not room:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "존재하지 않는 스터디룸입니다."
            )
        return room
    
    async def read_room_by_id_with_tools(self, db: AsyncSession, room_id: int):
        room = await room_repository.find_by_id_with_tools(db, room_id)
        if not room:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "존재하지 않는 스터디룸입니다."
            )
        return room
    
    async def update_room(self, db: AsyncSession, room_id: int, data: RoomCreate, current_user: User):
        if current_user.user_id != 1:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "관리자 권한이 없습니다."
            )

        async with db.begin():
            room = await self.read_room_by_id_with_tools(db, room_id)
            room.rooms_tools = []

            for name in data.tools:
                tool = await tool_repository.find_by_name(db, name)

                if not tool:
                    tool = Tool(name=name)
                    tool_repository.save(db, tool)
                    await db.flush()

                rooms_tools_link = RoomTool(tool=tool)
                room.rooms_tools.append(rooms_tools_link)

            updated_room = await room_repository.update(db, room, data)
                
        updated_room = await room_repository.find_by_id_with_tools(db, room_id)
        return updated_room

    async def delete_room(self, db: AsyncSession, room_id: int, current_user: User):
        if current_user.user_id != 1:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "관리자 권한이 없습니다."
            )
        
        async with db.begin():
            room = await self.read_room_by_id_with_tools(db, room_id)

            await room_repository.delete(db, room)

room_service = RoomService()