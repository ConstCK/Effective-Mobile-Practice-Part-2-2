# from __future__ import annotations
import datetime
from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base


class TradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    exchange_product_id: Mapped[int]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[int]
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[datetime.datetime]
    created_on: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), default=datetime.datetime.now())
    updated_on: Mapped[datetime.datetime] = mapped_column(default=func.now(),
                                                          server_default=func.now(),
                                                          onupdate=func.now())

    __table_args__ = (UniqueConstraint('date', 'exchange_product_id'),)
