from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from studyroom.models.reservation import Reservation

class ReservationRepository:
    def save(self, db: Session, reservation: Reservation):
        db.add(reservation)
        return reservation
    
    async def get_times_by_room_id_with_date(self, db: AsyncSession, room_id: int, target_date: date):
        stmt = select(Reservation.reservation_time).where(
            Reservation.room_id == room_id,
            Reservation.reservation_date == target_date
        )
        result = await db.scalars(stmt)
        return result.all()

reservation_repository = ReservationRepository()
