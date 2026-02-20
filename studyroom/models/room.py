from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .room_tool import RoomTool
    from .tool import Tool
    from .reservation import Reservation
    from .review import Review

class Room(Base):
    __tablename__ = "rooms"

    room_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    max_people: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(String(50), nullable=False)
    score_avg: Mapped[float] = mapped_column(default=0.0)

    reservation: Mapped[list["Reservation"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )

    rooms_tools: Mapped[list["RoomTool"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )

    # 논리적 지름길: post.tags 로 Tag 객체들에 바로 접근
    tools: AssociationProxy[list["Tool"]] = association_proxy("rooms_tools", "tool")