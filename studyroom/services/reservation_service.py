from datetime import time, date
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from studyroom.repositories.reservation_repository import reservation_repository
from studyroom.repositories.room_repository import room_repository
from studyroom.models.user import User
from studyroom.models.reservation import Reservation
from studyroom.schemas.reservation import ReservationCreate, ReservationSlot, ReservationReadResponse

class ReservationService:    
    async def add_room_reservation(self, db: AsyncSession, room_id: int, data: ReservationCreate, current_user: User):
        try:
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

        except IntegrityError:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 해당 시간에 예약이 존재합니다."
        )

        return {"message" : "예약 완료"}

    async def read_room_reservation(self, db: AsyncSession, room_id: int, target_date: date):
        START_HOUR = 9
        END_HOUR = 18
        async with db.begin():
            reservation_times = set(await reservation_repository.get_times_by_room_id_with_date(db, room_id, target_date))

            times = []
            for hour in range(START_HOUR, END_HOUR + 1):
                t = time(hour, 0)
                times.append(
                    ReservationSlot(reservation_time=t, available=t not in reservation_times)
                )
        
        return ReservationReadResponse(reservation_date=target_date, slots=times)


reservation_service = ReservationService()
