from datetime import datetime, date, time
from pydantic import BaseModel, ConfigDict

class ReservationCreate(BaseModel):
    reservation_date: date
    reservation_time: time
