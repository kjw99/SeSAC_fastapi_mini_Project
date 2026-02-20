from fastapi import APIRouter, Depends, status
from database import get_db
from async_database import get_async_db
from studyroom.models.user import User
from studyroom.dependencies import get_current_user
from studyroom.services.user_service import user_service
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from studyroom.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse,
)
from studyroom.schemas.reservation import ReservationCreate

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/auth/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate, db: AsyncSession = Depends(get_async_db)):
    return await user_service.signup(db, data)

@router.post("/auth/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_async_db)):
    access_token = await user_service.login(db, data)
    return {"access_token": access_token}
