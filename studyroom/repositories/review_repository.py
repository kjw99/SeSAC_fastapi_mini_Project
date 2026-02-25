from sqlalchemy.orm import Session
from studyroom.models.review import Review
from studyroom.models.reservation import Reservation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

class ReviewRepository:
    def save(self, db: Session, review: Review):
        db.add(review)
        return review

    async def get_avg_score_by_room_id(self, db: AsyncSession, room_id: int) -> float | None:
        stmt = (
            select(func.avg(Review.score))
            .join(Reservation, Review.reservation_id == Reservation.reservation_id)
            .where(Reservation.room_id == room_id)
        )
        result = await db.scalar(stmt)
        return float(result) if result is not None else None

    async def find_by_reservation_id(self, db: AsyncSession, reservation_id: int):
        stmt = select(Review).where(Review.reservation_id == reservation_id)
        result = await db.scalars(stmt)
        return result.first()

review_repository = ReviewRepository()