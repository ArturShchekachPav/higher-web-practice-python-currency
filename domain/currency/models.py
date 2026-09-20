from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base, CommonMixin


class Currency(Base, CommonMixin):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(String(3), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    nominal: Mapped[int] = mapped_column(nullable=False, default=1)

    rates: Mapped[list["ExchangeRate"]] = relationship(
        back_populates="currency",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Currency code={self.code} name={self.name}>"


class ExchangeRate(Base, CommonMixin):
    __tablename__ = "exchange_rates"
    __table_args__ = (
        UniqueConstraint("currency_id", "date", name="uq_currency_rate_date"),
    )

    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    rate: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    date: Mapped[date] = mapped_column(Date, index=True, nullable=False)

    currency: Mapped["Currency"] = relationship(back_populates="rates")

    def __repr__(self) -> str:
        return f"<ExchangeRate currency_id={self.currency_id} date={self.date} rate={self.rate}>"