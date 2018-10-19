import django
django.setup()
import scrapy
from ..items import ReviewItem
from atlas.models import Product, Review
import traceback
import re
import math

import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
from datetime import datetime
import random


# global max_rev_pgs

# To extract common URL prefix (for Review pages) from Product page URL
def get_review_url_prefix(p_url):
    # To prepare final prefix
    # print('p_url= ', p_url)
    p_url_1 = p_url.replace("/dp/", "/product-reviews/")
    start_index = len(p_url_1)
    for m in re.finditer('ref=', p_url_1):
        # print("inside for looop")
        start_index = m.start()
        break
    if not start_index == len(p_url_1):
        var_prefix = p_url_1[:start_index + 4]  # To extract common prefix from beginning of URL to 'ref='; hence +4
        common_suffix = "/cm_cr_dp_see_all_btm?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=recent&pageNumber="
        r_url = var_prefix + common_suffix
        # print(r_url)
        return r_url
    elif start_index == len(p_url_1):
        var_prefix = p_url_1   # To extract common prefix from beginning of URL to end (ends in ASIN)
        common_suffix = "/cm_cr_dp_see_all_btm?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=recent&pageNumber="
        r_url = var_prefix + common_suffix
        # print(r_url)
        return r_url


class AmazonReviewSpider(scrapy.Spider):
    print("inside amazonreviewspider")
    name = 'amazonreviewspider'

    allowed_domains = ["amazon.com"]

    def start_requests(self):
        # global max_rev_pgs
        try:
            # print(self.prod_urls_dict)
            prod_ids = self.prod_urls_dict.keys()
            # print(prod_ids)

            for p in prod_ids:
                try:
                    req = scrapy.Request(self.prod_urls_dict[p])
                    req.meta['pid'] = p
                    req.meta['kw'] = self.kw_str
                    yield req
                except:
                    print("error while creating req for rev scrape")
                    print(traceback.print_exc())

        except:
            print("error in start_req for rev scrape")
            print(traceback.print_exc())

    # start_urls = [
    #     "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=tv"
    # ]

    def parse(self, response):
        # global max_rev_pgs
        try:
            # print("inside parse() for amrevspider")
            # print("response.url = ", response.url)
            # print('pid in response = ', response.meta['pid'])
            # print('kw in response = ', response.meta['kw'])

            rev_urls = []
            rev_url_prefix = get_review_url_prefix(response.url)  # Obtain the common prefix for reviews, from product URL

            try:
                max_rev_pgs = str(response.xpath("//*[@id='acrCustomerReviewText']/text()").extract()[0]).split(" ")[0].split(",")
                max_rev_pgs = math.floor(int("".join(max_rev_pgs))/10)
            except:
                max_rev_pgs = 1
            # print("max_rev_pgs = ", max_rev_pgs)

            if max_rev_pgs >= 1:
                for i in range(1, int(max_rev_pgs) + 1):
                    rev_url = rev_url_prefix + str(i)  # Generate the URL by changing page number
                    rev_urls.append(rev_url)

            # print("Generated rev urls for this prod_url")
            # rev_urls = ["https://www.amazon.com/SuperSonic-1080p-Widescreen-Compatible-22-Inch/product-reviews/B0066AE4M8/ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews&pageNumber=1", "https://www.amazon.com/SuperSonic-1080p-Widescreen-Compatible-22-Inch/product-reviews/B0066AE4M8/ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews&pageNumber=2"]
            # print('rev_urls= ', rev_urls)

            for r in rev_urls:
                req = scrapy.Request(r, callback=self.parse_review)
                req.meta['pid'] = response.meta['pid']
                req.meta['kw'] = response.meta['kw']
                yield req

        except:
            print("Error in parse() of amrevspider")
            print(traceback.print_exc())

    def parse_review(self, response):
        # print("inside atlas parse_review()")
        print("response meta pid = === ", response.meta['pid'])

        try:
            for quote in response.xpath("//div[@id='cm_cr-review_list']"):
                # print("response pid = ", response.meta['pid'])
                # print("response kw = ", response.meta['kw'])

                rev_author = quote.xpath("//a[@data-hook='review-author']//text()").extract()
                max_len = len(rev_author)
                # print(max_len)
                for m in range(0, max_len):
                    item = ReviewItem()
                    try:
                        rev_author = quote.xpath("//a[@data-hook='review-author']//text()").extract()
                        item['rUser'] = rev_author[m]
                    except:
                        item['rUser'] = "#N/A"

                    try:
                        rev_title = quote.xpath("//a[@data-hook='review-title']//text()").extract()
                        item['rTitle'] = rev_title[m]
                    except:
                        item['rTitle'] = "#N/A"

                    try:
                        rev_date = quote.xpath("//span[@data-hook='review-date']//text()").extract()
                        rev_date = rev_date[m]
                        # Extracted date looks like 'on July 25, 2018'
                        rev_date = str(rev_date[3:])
                        # print("revdate before: ", rev_date)
                        if isinstance(rev_date, basestring):
                            rev_date = datetime.strptime(rev_date, "%B %d, %Y").strftime("%Y-%m-%d")
                        # print("revdate after: ", rev_date)
                        item['rDate2'] = rev_date
                        item['rDate'] = datetime.strptime(rev_date, '%Y-%m-%d')
                        # print(item['rDate'])
                        item['dt'] = datetime.strptime(rev_date, "%Y-%m-%d").day
                        # print(item['dt'])
                        item['mth'] = datetime.strptime(rev_date, "%Y-%m-%d").month
                        # print(item['mth'])
                        item['year'] = datetime.strptime(rev_date, "%Y-%m-%d").year
                        # print(item['year'])
                    except:
                        item['rDate2'] = '2000-01-01'
                        item['rDate'] = datetime.strptime(item['rDate2'], '%Y-%m-%d')
                        item['dt'] = '01'
                        item['mth'] = '01'
                        item['year'] = '2000'

                    try:
                        rev_text = quote.xpath("//span[@data-hook='review-body']/text()").extract()
                        item['rText'] = rev_text[m]
                    except:
                        item['rText'] = "#N/A"

                    try:
                        rev_rating = quote.xpath("//i[@data-hook='review-star-rating']//span/text()").extract()
                        rev_rating = rev_rating[m]
                        rev_rating = re.search(r'[0-9](.[0-9])?', str(rev_rating)).group(0)

                        item['rRating'] = rev_rating
                    except:
                        item['rRating'] = "0.0"

                    item['rURL'] = response.url

                    # try:
                    item['pid'] = Product.objects.get(pid=response.meta['pid'])
                    # except:
                    #     item['pid'] = str(random.randint(1, 99999)*0.1)
                    #     print(traceback.print_exc())
                    print(item['pid'])

                    # try:
                    item['rid'] = response.meta['kw'] + "_" + item['rUser'] + "_" + str(len(item['rText'])) + "_" + str(len(item['rTitle']))
                    # except:
                    #     item['rid'] = str(random.randint(1, 99999) * 0.1)
                    # print(item)
                    try:
                        item.save()
                    except:
                        print("Error in saving scraped review item")
                        print(traceback.print_exc())

                    yield item

        except:
            print("Error in parse_review()")
            print(traceback.print_exc())


# the wrapper to make it run more times
def f(q, prod_urls_dict, kw_str):
    try:
        runner = crawler.CrawlerRunner()
        # deferred = runner.crawl(AmazonReviewSpider, prod_urls=prod_urls, prod_ids=prod_ids, kw_str=kw_str)
        deferred = runner.crawl(AmazonReviewSpider, prod_urls_dict=prod_urls_dict, kw_str=kw_str)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


def run_spider(prod_urls_dict, kw_str):
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
    p = Process(target=f, args=(q, prod_urls_dict, kw_str))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

#
# print('first run:')
# run_spider()
#
# print('\nsecond run:')
# run_spider()  # the script will block here until the crawling is finished
