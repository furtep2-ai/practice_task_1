import uvicorn
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, HTTPException, Header, Depends, status
from database import Slot, AsyncSessionLocal, Booking , AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel, ConfigDict

app = FastAPI()

TOKENS = {
    "Demo-user-1": 1,
    "Demo-user-2": 2
}

class BookingRequest(BaseModel):
    slot_id: str

    model_config = ConfigDict(extra="forbid")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(x_demo_token: str = Header()):
    if x_demo_token not in TOKENS:
        raise HTTPException(status_code=401, detail="Invalid token")
    return TOKENS[x_demo_token]

@app.get("/slots")
async def get_slots(db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    result = await db.execute(select(Slot))
    slots = result.scalars().all()

    if not slots:
        return {"slots": []}
    
    slots_list = []
    for slot in slots:
        slots_list.append({
            "id": slot.id,
            "equipment_name" : slot.equipment_name,
            "label": slot.label,
            "available": slot.avaiable
        })
    return {"slots": slots_list}

#owner_id берется прямиком из токена
@app.post("/bookings/{slot_id}/book", status_code = status.HTTP_201_CREATED)
async def book_slot(request: BookingRequest, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
        slot_id = request.slot_id
        query = await db.execute(select(Slot).where(Slot.id == slot_id))
        result = query.scalar_one_or_none()

        if not result:
            raise HTTPException(status_code = 404, detail= "Not found slot_id")
        try: 
            with db.no_autoflush:
                booking = Booking(slot_id = slot_id, owner_id = current_user)
                db.add(booking)
                await db.execute(
                    update(Slot)
                    .where(Slot.id == slot_id)
                    .values(avaiable = False)
                )
        
            await db.commit()
            await db.refresh(booking)
        #2 и более пользователи могут одновременно забронировать что и приведет к ошибке UNIQUIE защита на уровне бд и не требует лишних затрат в коде
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code = 409, detail = "Slot already booked")

        return {"id": booking.id, "slot_id": slot_id}

@app.get("/bookings/{id}")
async def get_booking(id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    query = await db.execute(select(Booking).where(Booking.id == id))
    result = query.scalar_one_or_none()

    if not result:
        raise HTTPException(status_code = 404, detail= "Not found booking")

    if result.owner_id != current_user:
        raise HTTPException(status_code = 404, detail = "It isn't your booking")

    return {"id": result.id, "slot_id": result.slot_id}

@app.delete("/bookings/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(id: int, db: AsyncSession = Depends(get_db),current_user: str = Depends(get_current_user)):
    query = await db.execute(select(Booking).where(Booking.id == id))
    booking = query.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code = 404, detail= "Not found booking")

    if booking.owner_id != current_user:
        raise HTTPException(status_code = 404, detail = "It isn't your booking")

    await db.execute(
            update(Slot)
            .where(Slot.id == booking.slot_id)
            .values(avaiable=True)
        )

    await db.delete(booking)
    await db.commit()

@app.get("/my-bookings")
async def get_my_bookings(db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    query = await db.execute(select(Booking).where(Booking.owner_id == current_user))
    bookings = query.scalars().all()

    if not bookings:
        return {"Bookings": []}

    return {"Bookings": [
        {"id": b.id, "slot_id": b.slot_id, "owner_id": b.owner_id}
        for b in bookings
    ]}







        
            


        

        





   

            
