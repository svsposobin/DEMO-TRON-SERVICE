import asyncio
import pytest

from decimal import Decimal
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from databases.postgres.models import BaseMeta
from databases.postgres.utils import async_db_session
from src.tron.dto import TronDataResponse

from src.main import app

TEST_DB_DSN: str = "sqlite+aiosqlite:///./test.db"
TEST_ENGINE: AsyncEngine = create_async_engine(TEST_DB_DSN)
TEST_SESSION = sessionmaker(  # type: ignore
    bind=TEST_ENGINE,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def override_db_session():
    async with TEST_SESSION() as session:
        yield session


app.dependency_overrides[async_db_session] = override_db_session


@pytest.fixture
def mock_tron_service_for_integration():
    with patch("src.apis.dependencies.DEFAULT_TRON_SERVICE") as mock:
        mock.get_wallet_info = AsyncMock(return_value=TronDataResponse(
            address="TXYZ...",
            balance=Decimal("100"),
            bandwidth=5000,
            energy=2000
        ))
        yield mock


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    async def db_setup():
        async with TEST_ENGINE.begin() as conn:
            await conn.run_sync(BaseMeta.metadata.create_all)

    async def db_teardown():
        async with TEST_ENGINE.begin() as conn:
            await conn.run_sync(BaseMeta.metadata.drop_all)

    asyncio.run(db_setup())
    yield
    asyncio.run(db_teardown())


@pytest.fixture(autouse=True)
def clear_database():
    """Очищаем базу данных перед каждым тестом"""
    from databases.postgres.models import RequestedWallets
    import asyncio

    async def _clear():
        async with TEST_SESSION() as session:
            from sqlalchemy import delete
            await session.execute(delete(RequestedWallets))
            await session.commit()

    asyncio.run(_clear())


@pytest.mark.asyncio
async def test_add_record(mock_tron_service_for_integration):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/records/add/?address=TXYZ...")
        assert response.status_code == 200
        data = response.json()
        assert data["saved"] is True
        assert data["address"] == "TXYZ..."


@pytest.mark.asyncio
async def test_get_records(mock_tron_service_for_integration):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_check = await ac.get("/api/records/get/?page=1")
        data_check = response_check.json()
        print(f"Initial records count: {len(data_check['info'])}")

        response_add = await ac.post("/api/records/add/?address=TXYZ...")
        assert response_add.status_code == 200

        response = await ac.get("/api/records/get/?page=1")
        assert response.status_code == 200
        data = response.json()
        print(f"Records after add: {len(data['info'])}")
        print(f"Records data: {data['info']}")
        assert len(data["info"]) == 1
        assert data["info"][0]["address"] == "TXYZ..."
