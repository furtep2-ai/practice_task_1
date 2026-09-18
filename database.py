import sqlite3 as sq
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column , relationship
from sqlalchemy import UniqueConstraint, ForeignKey, Boolean, Integer, String

engine = create_async_engine('sqlite+aiosqlite:///my_database.db')

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    equipment_name: Mapped[str] = mapped_column(String, nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    avaiable:Mapped[bool] = mapped_column(Boolean, default=True)

    booking: Mapped["Booking"] = relationship(back_populates="slot")

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slot_id: Mapped[str] = mapped_column(String, ForeignKey("slots.id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    slot: Mapped["Slot"] = relationship(back_populates="booking")

    __table_args__ = (
        UniqueConstraint("slot_id", name="uq_slot_booking"),
    )






