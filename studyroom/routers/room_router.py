from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from studyroom.dependencies import get_current_user
from studyroom.models.user import User
from studyroom.schemas.room import RoomCreate, RoomResponse
from studyroom.services.room_service import room_service

router = APIRouter(prefix="/room", tags=["room"])


@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    data: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인한 유저 자동 주입
):
    return room_service.create_room(db, data, current_user)

@router.get("", response_model=list[RoomResponse])
def read_posts(db: Session = Depends(get_db)):
    return room_service.read_rooms(db)

@router.put("/{room_id}", response_model=RoomResponse)
def update_post(
    room_id: int,
    data: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 본인 확인용
):
    return room_service.update_room(db, room_id, data, current_user)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 본인 확인용
):
    room_service.delete_room(db, room_id, current_user)