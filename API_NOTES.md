Если заголовок отсутствует или токен неверный → `401 msg = 'Invalid token' ` для всех роутов.

Список методов API

1. GET('Slots') - Выдача всех слотов.

Сценарий_1 - Если нету слотов → `200` пустой список в формате {"slots": []}
Сценарий_2 - Если имеется слоты → вернется список слотов в таком формате
{slots: [
    {
        "id": slot.id,
        "equipment_name" : slot.equipment_name,
        "label": slot.label,
        "available": slot.avaiable
    }]
}

2. POST("/bookings/{slot_id}/book") - Бронирование слотов.

Сценарий_1 - Попытка передать в POST что-то помимо slot_id → `422 msg = 'Extra inputs are not permitted'`
Сценарий_2 - Отсуствие слота в бд → `404 msg = 'Not found slot_id'`
Сценарий_3 - Слот уже забронирован `409 msg = 'Slot already booked'`
Сценарий_4 - Слот забронировался → `201 created` вернет id брони {"id": booking.id, "slot_id": slot_id}

3. GET("/bookings/{id}") - Поиск брони

Сценарий_1 - Отсуствие брони в бд → `404 msg = 'Not found booking'`
Сценарий_2 - Чужая бронь → `404 msg = 'It isn't your booking'`
Сценарий_3 - Успех → `200 {"id": result.id, "slot_id": result.slot_id}`

4. DELETE("/bookings/{id}") - Удаление брони

Сценарий_1 - Отсуствие брони в бд → `404 msg = 'Not found booking'`
Сценарий_2 - Чужая бронь → `404 msg = 'It isn't your booking'`
Сценарий_3 - Успех → `204 NO_CONTENT`

5. GET("my-bookings) - Выдача всех броней текущего пользователя

Сценарий_1 - Отсуствие броней → `200` пустой список в формате {"Bookings": []}
Сценарий_2 - Успех return → `200` 
{"Bookings": [
    {"id": b.id, "slot_id": b.slot_id, "owner_id": b.owner_id}
    for b in bookings
]}