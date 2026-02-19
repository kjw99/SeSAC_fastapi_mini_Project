from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    hakbun: int
    password: str
    name: str
    phone: str

class UserResponse(BaseModel):
    user_id: int
    hakbun: int
    name: str
    phone: str

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    hakbun: int
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"