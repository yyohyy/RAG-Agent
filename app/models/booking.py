from sqlalchemy import Column, Integer, String, Date, Time

from app.config.database import Base

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)