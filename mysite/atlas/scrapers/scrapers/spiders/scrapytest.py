''' This is AmazonProductSpider.py '''

import django
django.setup()
import scrapy
from ..items import ProductItem
# from atlas.models import Product
import re
import traceback

import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
import urllib


global kw_str


class AmazonProductSpider(scrapy.Spider):

    print("inside amazonproductspider")
    name = 'amazonproductspider'

    allowed_domains = ["amazon.com"]

    def start_requests(self):
        try:
            print(self.kw_str)
            globals()['kw_str'] = self.kw_str
            # splits = str(self.kw_str).split("=")
            # globals()['kw_str'] = urllib.unquote(splits[len(splits) - 1].decode('utf-8', 'ignore'))
            # print(globals()['kw_str'])
            try:
                # max_sr_pgs = int(response.xpath('//*[@class="pagnDisabled"]/text()'))
                max_sr_pgs = 3
                # print("max_sr_pgs = ", max_sr_pgs)

                for i in range(1, max_sr_pgs + 1):
                    sr_url = "https://www.amazon.com/gp/search/ref=sr_pg_1?keywords=" + urllib.quote(self.kw_str) + "&page=" + str(i)  # search result url
                    # print(sr_url)
                    req = scrapy.Request(sr_url, callback=self.parse)
                    yield req
            except:
                print("error while creating 1st req")
                print(traceback.print_exc())

        except:
            print("error in start_req")
            print(traceback.print_exc())

    # start_urls = [
    #     "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=tv"
    # ]

    def parse(self, response):
        # print("inside parse()")
        try:

            r = response.xpath(
                "//ul[@id='s-results-list-atf']//li[contains(@id,'result_')]//div[@class='s-item-container']//a[@class='a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal']")

            for r1 in r:
                one_purl = r1.xpath("@href").extract()[0]
                # print one_purl
                try:
                    request = scrapy.Request(one_purl, callback=self.parse_product)
                    yield request
                except:
                    print("traceback in parse()")
                    print(traceback.print_exc())

        except:
            max_sr_pgs = 1

    def parse_product(self, response):
        # print("inside parse_product")
        global curr_pid
        item = ProductItem()
        # print(item)

        try:
            try:
                temp_title = response.xpath('//*[@id="productTitle"]/text()').extract()
                temp_title = temp_title[0].encode('utf-8', 'ignore').strip()
                item['pTitle'] = temp_title
            except:
                item['pTitle'] = "#N/A"

            try:
                temp_price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract()
                temp_price = temp_price[0].encode('utf-8', 'ignore')
                item['pPrice'] = temp_price
            except:
                item['pPrice'] = "#N/A"

            try:
                temp_brand = response.xpath('//*[@id="bylineInfo"]/text()').extract()
                temp_brand = temp_brand[0].encode('utf-8', 'ignore').strip()
                item['pBrand'] = temp_brand
            except:
                item['pBrand'] = "#N/A"

            try:
                temp_rating = response.xpath('//*[@id="acrPopover"]/@title').extract()
                item['pRating'] = re.search(r'[0-9](.[0-9])?', str(temp_rating)).group(0)
            except:
                item['pRating'] = "0.0"

            try:
                temp_imgsrc = response.xpath('//*[@id="landingImage"]/@src').extract()
                temp_imgsrc = temp_imgsrc[0].encode('utf-8', 'ignore').strip()
                item['pImgSrc'] = temp_imgsrc
            except:
                item['pImgSrc'] = "#"

            try:
                temp_descr = response.xpath('//*[@id="productDescription"]')
                temp_descr = temp_descr.xpath('string(.)').extract()
                item['pDescr'] = temp_descr[0].encode('utf-8', 'ignore').strip()
            except:
                item['pDescr'] = "Not available"

            try:
                item['pURL'] = response.url
            except:
                item['pURL'] = "#N/A"

            try:
                item['pModel'] = response.url[response.url.find("/dp/") + 4: response.url.find("/dp/") + 14]
                # +4 for ASIN begins after 4th character from "/dp/"; and +14 because ASIN is 10 characters long, starting from
                # start index and end index character is excluded
            except:
                item['pModel'] = "#N/A"

            item['pid'] = globals()['kw_str'] + "_" + item['pBrand'] + "_" + item['pModel']
            globals()['curr_pid'] = item['pid']
            # print('global pid inside parse_product = ', globals()['curr_pid'])

            item['pCategory'] = globals()['kw_str']

            item['siteCode'] = 'AM'

            # print(item)
            item.save()
            yield item

        except:
            print("Error in parse_review()")
            print(traceback.print_exc())


# the wrapper to make it run more times
def f(q, kw_str):
    try:
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(AmazonProductSpider, kw_str=kw_str)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


def run_spider(kw_str):
    # def f(q):
    #     try:
    #         runner = crawler.CrawlerRunner()
    #         # deferred = runner.crawl(QuotesSpider)
    #         deferred = runner.crawl(AmazonProductSpider)
    #         deferred.addBoth(lambda _: reactor.stop())
    #         reactor.run()
    #         q.put(None)
    #     except Exception as e:
    #         q.put(e)

    q = Queue()
    p = Process(target=f, args=(q, kw_str))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result
