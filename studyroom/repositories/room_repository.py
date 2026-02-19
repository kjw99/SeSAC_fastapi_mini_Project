# repositories/post_repository.py

from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from studyroom.models.room import Room
from studyroom.models.room_tool import RoomTool
from studyroom.schemas.room import RoomCreate

class RoomRepository:
    def save(self, db: Session, new_room: Room):
        # 세션의 작업 목록에 새로운 객체를 추가한다.
        db.add(new_room)
        return new_room

    def find_all(self, db: Session):
        # select 문을 생성하고 scalars를 통해 결과 객체들을 리스트로 가져온다.
        return db.scalars(select(Room)).all()
    
    def find_all_with_tools(self, db: Session):
        stmt = select(Room).options(selectinload(Room.rooms_tools).joinedload(RoomTool.tool))
        return db.scalars(stmt).all()

    def find_by_id(self, db: Session, room_id: int):
        # 기본키(Primary Key)를 이용한 조회는 db.get이 가장 빠르고 효율적이다.
        return db.get(Room, room_id)

    # def update(self, db: Session, room: Room, data: RoomCreate):
    #     # 이미 조회된 객체의 속성을 변경하면 세션이 이를 감지한다.
    #     post.title = data.title
    #     post.content = data.content
    #     return room

    # def delete(self, db: Session, room: Room):
    #     # 세션에서 해당 객체를 삭제 대상으로 표시한다.
    #     db.delete(room)

room_repository = RoomRepository()
