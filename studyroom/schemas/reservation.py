from datetime import datetime, date, time
from pydantic import BaseModel, ConfigDict, field_serializer

class ReservationCreate(BaseModel):
    reservation_date: date
    reservation_time: time

class ReservationSlot(BaseModel):
    reservation_time: time
    available: bool

    @field_serializer("reservation_time")
    def serialize_time(self, value: time):
        return value.strftime("%H:%M")

class ReservationReadResponse(BaseModel):
    reservation_date: date
    slots: list[ReservationSlot]


class MyReservationItem(BaseModel):
    reservation_id: int
    name: str
    date: date
    time: str
    state: bool

    @field_serializer("date")
    def serialize_date(self, value: date):
        return value.strftime("%Y-%m-%d")