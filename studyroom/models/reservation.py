from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .room import Room

class Reservation(Base):
    __tablename__ = "reservations"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room_id"), primary_key=True)
    reservation_date: Mapped[datetime.date] = mapped_column(
        Date, nullable=False
    )
    reservation_time: Mapped[datetime.time] = mapped_column(
        Time, nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="reservation")
    room: Mapped["Room"] = relationship(back_populates="reservation")