from datetime import date
from sqlalchemy.orm import Session, joinedload
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
    

    async def find_by_id(self, db: AsyncSession, reservation_id: int):
        return await db.get(Reservation, reservation_id)

    async def find_by_id_with_user(self, db: AsyncSession, reservation_id: int, user_id: int):
        stmt = select(Reservation).where(
            Reservation.reservation_id == reservation_id,
            Reservation.user_id == user_id
        )
        result = await db.scalar(stmt)
        return result

    async def find_all_by_user_id(self, db: AsyncSession, user_id: int):
        stmt = (
            select(Reservation)
            .where(Reservation.user_id == user_id)
            .options(joinedload(Reservation.room))
            .order_by(Reservation.reservation_date, Reservation.reservation_time)
        )
        result = await db.scalars(stmt)
        return result.all()

    async def delete(self, db: AsyncSession, reservation: Reservation):
        await db.delete(reservation)

reservation_repository = ReservationRepository()
