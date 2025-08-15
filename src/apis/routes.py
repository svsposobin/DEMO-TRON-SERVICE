from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.apis.dto import WriteRecordResponse, WalletsForPage
from src.apis.dependencies import write_wallet_info, get_wallet_info
from src.constants import RECORDS_PER_PAGE

router: APIRouter = APIRouter(prefix="/api", tags=["TRON-API"])


@router.get(
    path="/records/get/",
    response_class=JSONResponse,
    description=f"Получение записей, максимально {RECORDS_PER_PAGE} на страницу"
)
async def get_records(
        result: WalletsForPage = Depends(get_wallet_info),
):
    return result  # При необходимости можно добавить явную передачу статус-кодов


@router.post(
    path="/records/add/",
    response_class=JSONResponse,
    description="Добавление данных о TRON-Кошельке по адресу"
)
async def add_record(
        result: WriteRecordResponse = Depends(write_wallet_info),
):
    return result
