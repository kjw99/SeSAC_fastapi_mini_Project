from fastapi import APIRouter, Depends, status
from database import get_db
from async_database import get_async_db
from studyroom.models.user import User
from studyroom.dependencies import get_current_user
from studyroom.services.reservation_service import reservation_service
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from studyroom.schemas.reservation import ReservationCreate

router = APIRouter(prefix="/reservation", tags=["reservation"])

@router.post("/{room_id}", status_code=status.HTTP_201_CREATED)
async def add_room_reservation(
    room_id: int, 
    data: ReservationCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await reservation_service.add_room_reservation(db, room_id, data, current_user)