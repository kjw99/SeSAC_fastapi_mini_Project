from pydantic import BaseModel

class ReviewCreate(BaseModel):
    content: str
    score: int