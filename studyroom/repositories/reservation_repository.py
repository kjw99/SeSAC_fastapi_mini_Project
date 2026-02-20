from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from studyroom.models.reservation import Reservation

class ReservationRepository:
    def save(self, db: Session, reservation: Reservation):
        db.add(reservation)
        return reservation

reservation_repository = ReservationRepository()
