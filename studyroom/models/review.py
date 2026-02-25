from datetime import datetime

from sqlalchemy import DateTime, func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .reservation import Reservation

class Review(Base):
    __tablename__ = "reviews"

    review_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.reservation_id"), unique=True, nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    reservation: Mapped["Reservation"] = relationship(back_populates="review")
