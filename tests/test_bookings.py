import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import httpx2
from fastapi.testclient import TestClient
from app import app, BookingRequest


def test_without_token(client):
    response = client.get("/slots", headers={"X-Demo-Token": "Demo-user"})
    assert response.status_code == 401

def test_booking_conflict(client):
    response = client.post("/bookings/S1/book", headers={"X-Demo-Token": "Demo-user-2"}, json={
    "slot_id": "S1",
    "owner_id": 1})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert len(data["detail"]) > 0
    print(data["detail"])
    assert data["detail"][0]["msg"] == 'Extra inputs are not permitted'

    first = client.post("/bookings/S1/book", headers={"X-Demo-Token": "Demo-user-2"}, json={"slot_id": "S1"})
    assert first.status_code == 201

    response = client.post("/bookings/S1/book", headers={"X-Demo-Token": "Demo-user-2"}, json={"slot_id": "S1"})
    assert response.status_code == 409

def test_reading_deleteing_book(client):
    response = client.post("/bookings/S1/book", headers={"X-Demo-Token": "Demo-user-2"}, json={"slot_id": "S1"})
    assert response.status_code == 201

    response = client.get("/bookings/1", headers={"X-Demo-Token": "Demo-user-1"})
    assert response.status_code == 404

    response = client.delete("/bookings/1", headers={"X-Demo-Token": "Demo-user-2"})
    assert response.status_code == 204

def test_get_my_bookings(client):
    response = client.post("/bookings/S1/book", headers={"X-Demo-Token": "Demo-user-2"}, json={"slot_id": "S1"})
    assert response.status_code == 201

    response = client.post("/bookings/S2/book", headers={"X-Demo-Token": "Demo-user-2"}, json={"slot_id": "S2"})
    assert response.status_code == 201

    response = client.get("/my-bookings", headers={"X-Demo-Token": "Demo-user-2"})
    assert response.status_code == 200
    data = response.json()
    assert "Bookings" in data
    assert isinstance(data["Bookings"], list)
    assert len(data["Bookings"]) == 2

    response = client.get("/my-bookings", headers={"X-Demo-Token": "Demo-user-1"})
    assert response.status_code == 200

    data = response.json()
    assert "Bookings" in data
    assert data["Bookings"] == []






    


