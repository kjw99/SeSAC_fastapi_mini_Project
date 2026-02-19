from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .room_tool import RoomTool

class Tool(Base):
    __tablename__ = "tools"

    tool_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    rooms_tools: Mapped[list["RoomTool"]] = relationship(back_populates="tool")
