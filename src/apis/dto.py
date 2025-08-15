from typing import Optional, List

from pydantic import BaseModel

from src.tron.dto import TronDataResponse


class WriteRecordResponse(BaseModel):
    address: Optional[str] = None
    saved: bool = False

    error: Optional[str] = None


class WalletsForPage(BaseModel):
    info: List[TronDataResponse] = []

    error: Optional[str] = None
