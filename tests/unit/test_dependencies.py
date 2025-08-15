import pytest

from typing import Generator
from decimal import Decimal
from unittest.mock import MagicMock, AsyncMock, patch

from sqlalchemy.ext.asyncio import AsyncSession
from tronpy.exceptions import AddressNotFound  # type: ignore

from src.apis.dependencies import write_wallet_info
from src.apis.dto import WriteRecordResponse
from src.tron.dto import TronDataResponse
from src.tron.service import TronService


@pytest.fixture(scope="function")
def mock_session() -> Generator[AsyncMock, None, None]:
    session = AsyncMock(spec=AsyncSession)
    yield session


@pytest.fixture(scope="function")
def mock_tron_service() -> Generator[AsyncMock, None, None]:
    with patch.object(target=TronService, attribute="get_wallet_info", new_callable=AsyncMock) as mock:
        yield mock


@pytest.mark.asyncio
class TestWriteWalletInfo:
    async def test_write_wallet_info_success(self, mock_tron_service: AsyncMock, mock_session: AsyncMock) -> None:
        mock_response = MagicMock(spec=TronDataResponse)
        mock_response.address = "Mock-address-1234567890qwertyuiop["
        mock_response.balance = Decimal("100")
        mock_response.energy = 0
        mock_response.bandwidth = 0

        mock_tron_service.return_value = mock_response

        result: WriteRecordResponse = await write_wallet_info(
            address="Mock-address-1234567890qwertyuiop[",
            session=mock_session
        )

        assert result.error is None

        assert result.address == mock_response.address
        assert result.saved is True

    async def test_write_wallet_info_failure(self, mock_tron_service, mock_session) -> None:
        mock_tron_service.side_effect = AddressNotFound(
            "Адрес не был найден"
        )

        result: WriteRecordResponse = await write_wallet_info(
            address="Unvd-address-1234567890qwertyuiop[",
            session=mock_session
        )

        assert result.error == "Адрес не был найден"
        assert result.address is None
        assert result.saved is False

# Тест на получение записи не прописан в условиях тестового задания
