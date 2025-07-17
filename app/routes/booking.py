from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import date, time
from app.config.database import SessionLocal
from app.models.booking import Booking
from app.services.booking_service import BookingService

booking_router = APIRouter()
booking_service = BookingService()

class BookingIn(BaseModel):
    full_name:str; email:EmailStr; date:date; time:time

@booking_router.post("/book")
async def book(slot:BookingIn, tasks:BackgroundTasks):
    print(slot)
    with SessionLocal() as db:
        if db.query(Booking).filter_by(date=slot.date, time=slot.time).first():
            raise HTTPException(409,"Slot taken")
        db.add(Booking(**slot.model_dump())); db.commit()
    tasks.add_task(booking_service.send_confirmation, slot.email, slot.full_name, slot.date, slot.time)
    return{"Status":True}



