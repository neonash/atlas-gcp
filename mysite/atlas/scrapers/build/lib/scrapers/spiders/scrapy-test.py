import scrapy
from scrapers.items import ScraperItem, ProductItem


class Quotes(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = [
        "http://quotes.toscrape.com/"
    ]

    def parse(self, response):

        for sel in response.xpath('//div[@class="quote"]/span[@class="text"]::text'):
            item = ScraperItem()
            qt = sel.extract()
            item['qt'] = qt

            yield item
        if ".toscrape" in response.url:
            from scrapy.shell import inspect_response
            inspect_response(response, self)

# class ProductSpider(BaseSpider):
#     name = 'productspider'