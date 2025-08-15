from typing import Dict, Any
from dotenv import load_dotenv, find_dotenv
from os import getenv as os_getenv

load_dotenv(find_dotenv(".env.test"))

POSTGRES_POOL_SIZE = 5  # Max количество постоянных соединений
POSTGRES_MAX_OVERFLOW = 10  # Дополнительные соединения при нагрузке
POSTGRES_POOL_TIMEOUT = 30  # Время ожидания соединения (сек)
POSTGRES_POOL_RECYCLE = 300  # Пересоздавать соединения каждые N секунд

TRON_API_KEY_LIST: Dict[str, Any] = {
    "BASE_TRON_KEY": os_getenv("BASE_TRON_KEY"),
}

RECORDS_PER_PAGE: int = 10

API_DOC_METADATA: Dict[str, Any] = {
    "title": "TRON WALLETS HANDLER",
    "description": "Сервис по работе с TRON-Кошельками",
    "version": "1.0.0",
}
