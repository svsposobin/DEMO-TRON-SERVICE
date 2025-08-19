from fastapi import Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from databases.postgres.utils import async_db_session
from src.constants import RECORDS_PER_PAGE
from src.tron.dto import TronDataResponse
from src.apis.dto import WriteRecordResponse, WalletsForPage
from src.tron.service import DEFAULT_TRON_SERVICE
from databases.postgres.models import RequestedWallets


async def write_wallet_info(
        address: str = Query(),
        session: AsyncSession = Depends(async_db_session)
) -> WriteRecordResponse:
    result: WriteRecordResponse = WriteRecordResponse()

    try:
        tron_account_response: TronDataResponse = await DEFAULT_TRON_SERVICE.get_wallet_info(
            address=address,
        )

        async with session.begin():
            new_record: RequestedWallets = RequestedWallets(
                address=address,
                balance=tron_account_response.balance,
                bandwidth=tron_account_response.bandwidth,
                energy=tron_account_response.energy,

            )
            session.add(new_record)

        result.address = address
        result.saved = True

    except Exception as error:
        result.error = str(error)  # Можно реализовать маппинг ошибок

    return result


async def get_wallet_info(
        page: int = Query(default=1),
        session: AsyncSession = Depends(async_db_session)
):
    result: WalletsForPage = WalletsForPage()

    try:
        if page <= 0:
            result.error = "Страница не может быть меньше или равная нулю!"
            # Можно дополнительно добавить проверку на max. кол-во страниц

            return result

        limit: int = RECORDS_PER_PAGE
        offset: int = (page - 1) * limit

        async with session.begin():
            records_per_pagination = await session.scalars(
                select(RequestedWallets).offset(offset).limit(limit)
            )

            for record in records_per_pagination.all():
                result.info.append(
                    TronDataResponse(
                        address=record.address,
                        balance=record.balance,
                        bandwidth=record.bandwidth,
                        energy=record.energy,
                    )
                )

    except Exception as error:
        result.error = str(error)

    return result
