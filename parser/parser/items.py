import scrapy


class CurrencyItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    nominal = scrapy.Field()
    rate = scrapy.Field()
    date = scrapy.Field()
