from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from studyroom.repositories.reservation_repository import reservation_repository
from studyroom.repositories.room_repository import room_repository
from studyroom.models.user import User
from studyroom.models.reservation import Reservation
from studyroom.schemas.reservation import ReservationCreate

class ReservationService:    
    async def add_room_reservation(self, db: AsyncSession, room_id: int, data: ReservationCreate, current_user: User):
        
        async with db.begin():
            room = await room_repository.find_by_id_with_tools(db, room_id)
            if not room:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "잘못된 스터디룸 id입니다."
                )
            new_reservation = Reservation(
                reservation_date = data.reservation_date,
                reservation_time = data.reservation_time,
                user_id = current_user.user_id,
                room_id = room.room_id
            )
            reservation_repository.save(db, new_reservation)

        return {"message" : "예약 완료"}


reservation_service = ReservationService()
