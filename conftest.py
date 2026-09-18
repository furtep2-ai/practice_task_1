import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app import app, get_db
from database import Base, Slot


@pytest.fixture(scope="function")
def override_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    TestingSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal() as session:
            session.add_all([
                Slot(id="S1", equipment_name="Camera", label="Slot 1", avaiable=True),
                Slot(id="S2", equipment_name="Microphone", label="Slot 2", avaiable=True),
                Slot(id="S3", equipment_name="Tripod", label="Slot 3", avaiable=True),
            ])
            await session.commit()

    import asyncio
    asyncio.run(init_models())

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def client(override_session):
    with TestClient(app) as c:
        yield c