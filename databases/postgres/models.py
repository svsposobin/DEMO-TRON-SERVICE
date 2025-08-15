from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, DateTime, func, Numeric
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class BaseMeta(DeclarativeBase):
    pass


class RequestedWallets(BaseMeta):
    __tablename__: str = "requested_wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Unique осознанно не используется для множественного просмотра: когда и какой кошелек был записан
    address: Mapped[str] = mapped_column(String(length=34))

    balance: Mapped[Decimal] = mapped_column(Numeric(precision=30, scale=6))
    bandwidth: Mapped[int] = mapped_column(default=0)
    energy: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Дата записи в UTC. Автоматически конвертируется в local-time при чтении"
    )
