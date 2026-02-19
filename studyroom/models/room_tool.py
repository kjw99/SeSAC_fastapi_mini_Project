# models/post_tag.py

from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .room import Room
    from .tool import Tool

class RoomTool(Base):
    __tablename__ = "rooms_tools"
    
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room_id"), primary_key=True)
    tool_id: Mapped[int] = mapped_column(ForeignKey("tools.tool_id"), primary_key=True)

    room: Mapped["Room"] = relationship(back_populates="rooms_tools")
    tool: Mapped["Tool"] = relationship(back_populates="rooms_tools")