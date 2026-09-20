from datetime import date, timedelta
from parser.items import CurrencyItem

import scrapy


class CbrSpider(scrapy.Spider):
    name = "cbr"
    allowed_domains = ["cbr.ru"]
    URL_TEMPLATE = (
        "http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}"
    )

    def __init__(self, days: int = 30, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.days = int(days)
        self.seen_dates = set()

    def start_requests(self):
        today = date.today()
        for offset in range(self.days):
            target = today - timedelta(days=offset)
            url = self.URL_TEMPLATE.format(
                day=target.strftime("%d"),
                month=target.strftime("%m"),
                year=target.strftime("%Y"),
            )
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        date_str = response.xpath("//ValCurs/@Date").get()
        if not date_str or date_str in self.seen_dates:
            return
        self.seen_dates.add(date_str)

        day, month, year = date_str.split(".")
        rate_date = date(int(year), int(month), int(day))

        for valute in response.xpath("//Valute"):
            code = valute.xpath("CharCode/text()").get()
            name = valute.xpath("Name/text()").get()
            nominal_raw = valute.xpath("Nominal/text()").get()
            value_raw = valute.xpath("Value/text()").get()

            if not (code and name and nominal_raw and value_raw):
                continue

            nominal = int(nominal_raw)
            value = float(value_raw.replace(",", "."))
            rate = value / nominal

            yield CurrencyItem(
                code=code.strip(),
                name=name.strip(),
                nominal=nominal,
                rate=rate,
                date=rate_date,
            )
