from fastapi import APIRouter, Depends, status
from database import get_db
from async_database import get_async_db
from studyroom.models.user import User
from studyroom.dependencies import get_current_user
from studyroom.schemas.review import ReviewCreate
from studyroom.services.review_service import review_service
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/review", tags=["review"])

@router.post("/{reservation_id}", status_code=status.HTTP_201_CREATED)
async def create_review(
    reservation_id: int,
    data: ReviewCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await review_service.create_review(db, reservation_id, data, current_user)