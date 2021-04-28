import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Customer(Base):
    __tablename__= 'customer'

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(50))
    phone = Column(String(15))
    zip_code = Column(String(5))


class Booking(Base):
    __tablename__ = 'booking'

    booking_id = Column(Integer, primary_key=True)
    room_number = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    arrival = Column(Date)
    nights = Column(Integer)


class Invoice(Base):
    __tablename__ = 'invoice'

    invoice_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('booking.booking_id'))
    amount = Column(Float)
    paid = Column(Integer)
    paid_date = Column(Date)


class Room(Base):
    __tablename__ = 'room'

    room_number = Column(Integer, primary_key=True)
    floor = Column(Integer)
    room_type_id = Column(Integer, ForeignKey('room_type.room_type_id'))
    available = Column(Integer)


class RoomType(Base):
    __tablename__ = 'room_type'

    room_type_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    capacity = Column(Integer)
    price = Column(Float)


class BookingFee(Base):
    __tablename__ = 'booking_fee'

    booking_id = Column(Integer, ForeignKey('booking.booking_id'), primary_key=True)
    fee_id = Column(Integer, ForeignKey('fee.fee_id'), primary_key=True)
    quantity = Column(Integer)


class Fee(Base):
    __tablename__ = 'fee'

    fee_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Float(precision=2))
