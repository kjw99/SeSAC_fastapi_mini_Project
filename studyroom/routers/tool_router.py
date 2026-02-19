
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from studyroom.schemas.tool import ToolCreate, ToolResponse
from studyroom.services.tool_service import tool_service

router = APIRouter(prefix="/tool", tags=["tools"])

@router.post("", response_model=ToolResponse, status_code=status.HTTP_201_CREATED)
def create_tool(data: ToolCreate, db: Session = Depends(get_db)):
    return tool_service.create_tool(db, data)

@router.get("", response_model=list[ToolResponse])
def read_tools(db: Session = Depends(get_db)):
    return tool_service.read_tools(db)