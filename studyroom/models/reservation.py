from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey, Date, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .room import Room

class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room_id"))
    reservation_date: Mapped[datetime.date] = mapped_column(
        Date, nullable=False
    )
    reservation_time: Mapped[datetime.time] = mapped_column(
        Time, nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="reservation")
    room: Mapped["Room"] = relationship(back_populates="reservation")

    __table_args__ = (
        UniqueConstraint(
            "room_id",
            "reservation_date",
            "reservation_time",
            name="uq_room_datetime"
        ),
    )