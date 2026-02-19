from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from studyroom.repositories.room_repository import room_repository
from studyroom.repositories.tool_repository import tool_repository
from studyroom.models.room import Room
from studyroom.models.tool import Tool
from studyroom.models.room_tool import RoomTool
from studyroom.schemas.room import RoomCreate
from studyroom.models.user import User


class RoomService:
    def create_room(self, db: Session, data: RoomCreate, current_user: User):
        new_room = Room(
            name=data.name,
            max_people=data.max_people,
            location=data.location
        )

        with db.begin():
            for name in data.tools:
                tool = tool_repository.find_by_name(db, name)

                if not tool:
                    tool = Tool(name=name)
                    tool_repository.save(db, tool)
                    db.flush()  # ID 할당을 위해 flush 호출

                # 3. 연결 모델(PostTag) 생성 및 게시글에 추가
                # cascade 설정 덕분에 post_tags에 추가만 하면 나중에 함께 저장된다.
                rooms_tools_link = RoomTool(room=new_room, tool=tool)
                new_room.rooms_tools.append(rooms_tools_link)
                
                # 사용자에게 입력받는 추가 컬럼이 없는 경우 아래의 코드도 가능하다.
                # new_post.tags.append(tag)

            # 4. 게시글 저장 (연결된 PostTag들도 함께 저장됨)
            room_repository.save(db, new_room)

        db.refresh(new_room)
        return new_room
    
    # def read_posts(self, db: Session):
    #     return post2_repository.find_all(db)

    # def read_room_by_id(self, db: Session, room_id: int):
    #     room = room_repository.find_by_id(db, room_id)
    #     if not room:
    #         raise HTTPException(
    #             status.HTTP_404_NOT_FOUND, "존재하지 않는 스터디룸입니다."
    #         )
    #     return room
    
    # def update_post(self, db: Session, id: int, data: Post2Create, current_user: User):
    #     post = self.read_post_by_id(db, id)

    #     # 작성자 본인만 수정 가능
    #     if post.user_id != current_user.id:
    #         raise HTTPException(
    #             status.HTTP_403_FORBIDDEN, "본인의 게시글만 수정할 수 있습니다."
    #         )

    #     updated_post = post2_repository.update(db, post, data)
    #     db.commit()
    #     db.refresh(updated_post)
    #     return updated_post

    # def delete_post(self, db: Session, id: int, current_user: User):
    #     post = self.read_post_by_id(db, id)

    #     # 작성자 본인만 삭제 가능
    #     if post.user_id != current_user.id:
    #         raise HTTPException(
    #             status.HTTP_403_FORBIDDEN, "본인의 게시글만 삭제할 수 있습니다."
    #         )

    #     post2_repository.delete(db, post)
    #     db.commit()


room_service = RoomService()