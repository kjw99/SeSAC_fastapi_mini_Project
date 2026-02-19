from datetime import datetime
from pydantic import BaseModel, ConfigDict
from studyroom.schemas.tool import ToolResponse

class RoomCreate(BaseModel):
    name: str
    max_people: int
    location: str
    tools: list[str] = []

class RoomResponse(BaseModel):
    room_id: int
    name: str
    max_people: int
    location: str
    tools: list[ToolResponse] = []

    model_config = ConfigDict(from_attributes=True)
