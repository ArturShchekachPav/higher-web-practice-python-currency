from domain.currency.models import Currency, ExchangeRate
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.currency.exceptions import CurrencyNotFoundError, ExchangeRateNotFoundError


class CurrencyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_currencies(self) -> list[Currency]:
        """Получить все доступные валюты.

        :return: Список всех объектов валют
        """
        result = await self.session.execute(select(Currency))
        return list(result.scalars().all())

    async def get_latest_rate(self, target_code: str) -> ExchangeRate:
        """Получить последний курс обмена для определенной валюты.

        :param target_code: Код валюты (например, 'USD', 'EUR')
        :return: Последний объект курса обмена
        """
        currency = await self._get_currency_by_code(target_code)
        result = await self.session.execute(
            select(ExchangeRate)
            .join(Currency)
            .where(Currency.id == currency.id)
            .order_by(ExchangeRate.date.desc())
            .limit(1)
        )
        exchange_rate = result.scalar_one_or_none()
        if exchange_rate is None:
            raise ExchangeRateNotFoundError(
                f"Курс для валюты с кодом {target_code} не найден!"
            )
        return exchange_rate


    async def get_rate_history(
        self,
        target_code: str,
        start_date: date,
        end_date: date,
    ) -> list[ExchangeRate]:
        """Получить исторические курсы обмена для определенной валюты.

        :param target_code: Код валюты (например, 'USD', 'EUR')
        :param start_date: Дата начала в формате YYYY-MM-DD
        :param end_date: Дата окончания в формате YYYY-MM-DD
        :return: Список объектов курса обмена за указанный период
        """
        currency = await self._get_currency_by_code(target_code)
        result = await self.session.execute(
            select(ExchangeRate)
            .join(Currency)
            .where(
                Currency.id == currency.id,
                ExchangeRate.date >= start_date,
                ExchangeRate.date <= end_date
            )
            .order_by(ExchangeRate.date.asc())
        )
        return list(result.scalars().all())

    async def get_rates_for_currency(self, target_code: str) -> list[ExchangeRate]:
        """Получить все курсы обмена для определенной валюты (полная история).

        :param target_code: Код валюты (например, 'USD', 'EUR')
        :return: Список всех объектов курса обмена для валюты
        """
        currency = await self._get_currency_by_code(target_code)
        result = await self.session.execute(
            select(ExchangeRate)
            .join(Currency)
            .where(Currency.id == currency.id)
            .order_by(ExchangeRate.date.asc())
        )
        return list(result.scalars().all())

    async def _get_currency_by_code(self, target_code: str) -> Currency:
        result = await self.session.execute(
            select(Currency).where(Currency.code == target_code)
        )
        currency = result.scalar_one_or_none()
        if currency is None:
            raise CurrencyNotFoundError(
                f"Валюта с кодом {target_code} не найдена!"
            )
        return currency
