from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class TronDataResponse(BaseModel):
    address: Optional[str] = None
    balance: Optional[Decimal] = None
    bandwidth: Optional[int] = None
    energy: Optional[int] = None
