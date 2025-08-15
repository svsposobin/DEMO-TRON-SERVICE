from typing import Dict, Any

from tronpy import Tron  # type: ignore
from tronpy.providers import HTTPProvider  # type: ignore
from tronpy.exceptions import AddressNotFound  # type: ignore

from src.tron.dto import TronDataResponse
from src.constants import TRON_API_KEY_LIST


class TronService:
    def __init__(self, api_key: str):
        self.client = Tron(HTTPProvider(api_key=api_key))

    async def get_wallet_info(self, address: str) -> TronDataResponse:
        result: TronDataResponse = TronDataResponse()

        try:
            account: Dict[str, Any] = self.client.get_account(address)

            result.address = address
            result.balance = self.client.get_account_balance(address)
            result.bandwidth = account.get("free_net_limit", 0)
            result.energy = account.get("energy_limit", 0)

        except AddressNotFound:
            raise AddressNotFound("Адрес не был найден")

        except Exception as error:
            raise Exception(f"Что-то пошло не так, перепроверьте адрес. Детали: {error}")

        return result


DEFAULT_TRON_SERVICE: TronService = TronService(api_key=TRON_API_KEY_LIST["BASE_TRON_KEY"])
