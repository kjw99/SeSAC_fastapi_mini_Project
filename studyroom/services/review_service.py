from sqlalchemy.ext.asyncio import AsyncSession
from studyroom.schemas.review import ReviewCreate
from studyroom.models.user import User
from studyroom.repositories.review_repository import review_repository
from studyroom.models.review import Review
from studyroom.repositories.reservation_repository import reservation_repository
from studyroom.repositories.room_repository import room_repository
from fastapi import HTTPException, status
from datetime import datetime, timedelta

class ReviewService:
    async def create_review(self, db: AsyncSession, reservation_id: int, data: ReviewCreate, current_user: User):
        async with db.begin():
            review = await review_repository.find_by_reservation_id(db, reservation_id)
            if review:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="이미 리뷰를 작성하였습니다."
                )

            reservation = await reservation_repository.find_by_id(db, reservation_id)
            if not reservation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="예약 정보를 찾을 수 없습니다."
                )
            
            if reservation.user_id != current_user.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="본인의 예약에 대해서만 리뷰를 작성할 수 있습니다."
                )
            
            reservation_datetime = datetime.combine(reservation.reservation_date, reservation.reservation_time)
            if reservation_datetime + timedelta(hours=1) > datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="스터디룸 사용 이후에 리뷰를 작성할 수 있습니다."
                )

            new_review = Review(
                reservation_id=reservation_id,
                content=data.content,
                score=data.score
            )
            review_repository.save(db, new_review)
            await db.flush()

            room_id = reservation.room_id
            avg = await review_repository.get_avg_score_by_room_id(db, room_id)
            avg = avg if avg is not None else 0.0
            room = await room_repository.find_by_id(db, room_id)
            room.score_avg = round(avg, 2)

        return {"message": "리뷰 작성 완료"}

review_service = ReviewService()