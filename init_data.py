from database import AsyncSessionLocal, Slot, User, Booking, Base, engine
from sqlalchemy import select, delete
import asyncio

async def insert_data():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Slot))
        slots = result.scalars().all()

        if not slots:
            s1 = Slot(id = "S1",equipment_name="Учебный микрофон", label="Демонстрационный слот А")
            s2 = Slot(id = "S2" ,equipment_name="Учебный монитор" , label="Демонстрационный слот B")
            s3 = Slot(id = "S3" ,equipment_name="Учебный телефон" , label="Демонстрационный слот С")
            session.add_all([s1,s2,s3])

        result = await session.execute(select(User))
        users = result.scalars().all()

        if not users:
            u1 = User(name = "Demo User1")
            u2 = User(name = "Demo User2")
            session.add_all([u1, u2])

        await session.commit()

async def database_create():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_datA(book_id: int):
    async with AsyncSessionLocal() as session:
        query = await session.execute(delete(Booking).where(Booking.id == book_id))
        await session.commit()



if __name__ == "__main__":
    asyncio.run(insert_data())