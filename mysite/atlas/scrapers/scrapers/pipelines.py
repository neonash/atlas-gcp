import scrapy
from scrapers.items import ScraperItem
import json
from atlas.models import Product, Review
from datetime import datetime
import arrow

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AmazonProductPipeline(object):
    print("inside amazonproductpipeline")

    def process_item(self, item, spider):
        print("inside processitem")
        try:
            product = Product.objects.get(pid=item["pid"])
            print "Product already exist"
            return item
        except Product.DoesNotExist:
            print("Product deosnt exist. creating new record")
            pass

        product = Product()
        product.pTitle = item['pTitle']
        product.pPrice = item['pPrice']
        product.pBrand = item['pBrand']
        product.pRating = item['pRating']
        product.pImgSrc = item['pImgSrc']
        product.pDescr = item['pDescr']
        product.pURL = item['pURL']
        product.pModel = item['pModel']
        product.pid = item['pid']
        product.pCategory = item['pCategory']
        product.siteCode = item['siteCode']
        product.save()
        return item


class AmazonReviewPipeline(object):
    print("inside amazonreviewpipeline")

    def process_item(self, item, spider):
        print("inside processitem")
        try:
            review = Review.objects.get(rid=item["rid"])
            print "Review already exists"
            return item
        except Review.DoesNotExist:
            print("Review doesnt exist. creating new record")
            pass

        review = Review()
        review.rText = item['rText']
        review.rTitle = item['rTitle']
        review.rRating = item['rRating']
        review.rURL = item['rURL']

        review.dt = item['dt']
        review.mth = item['mth']
        review.year = item['year']
        # if isinstance(item['rDate2'], basestring):
        #     item['rDate2'] = datetime.strptime(item['rDate2'], "%Y-%m-%d")
        #
        # # print(item['rDate2'])
        # review.dt = item['rDate2'].day
        # review.mth = item['rDate2'].month
        # review.year = item['rDate2'].year
        # try:
        #     review.rDate = int(item['rDate2'].timestamp())
        # except:
        #     review.rDate = item['rDate2']

        review.rid = item['rid']
        review.rUser = item['rUser']
        review.pid = Product.objects.get(pid=item['pid'])
        review.save()

        return item

