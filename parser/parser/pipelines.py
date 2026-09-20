from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from core.config import settings
from domain.currency.models import Currency, ExchangeRate


class DatabasePipeline:
    def open_spider(self, spider):
        url = settings.database_url.replace("+asyncpg", "+psycopg")
        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)
        self.item_count = 0
        self.error_count = 0

    def close_spider(self, spider):
        spider.logger.info(
            f"Pipeline finished: {self.item_count} items, {self.error_count} errors"
        )
        if self.item_count > 0 and self.error_count / self.item_count > 0.5:
            raise RuntimeError(
                f"Too many errors: {self.error_count}/{self.item_count}"
            )
        self.engine.dispose()

    def process_item(self, item, spider):
        self.item_count += 1
        try:
            with self.Session() as session:
                currency = session.execute(
                    select(Currency).where(Currency.code == item["code"])
                ).scalar_one_or_none()

                if currency is None:
                    currency = Currency(
                        code=item["code"],
                        name=item["name"],
                        nominal=item["nominal"],
                    )
                    session.add(currency)
                    session.flush()

                existing = session.execute(
                    select(ExchangeRate).where(
                        ExchangeRate.currency_id == currency.id,
                        ExchangeRate.date == item["date"],
                    )
                ).scalar_one_or_none()

                if existing is None:
                    session.add(
                        ExchangeRate(
                            currency_id=currency.id,
                            rate=item["rate"],
                            date=item["date"],
                        )
                    )
                else:
                    existing.rate = item["rate"]

                session.commit()
        except Exception as e:
            self.error_count += 1
            spider.logger.error(f"Failed to save item {dict(item)}: {e}")

        return item
