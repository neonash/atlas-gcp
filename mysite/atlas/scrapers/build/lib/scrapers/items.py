# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from atlas.models import Product


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    qt = scrapy.Field()
    # pass


class ProductItem(DjangoItem):
    django_model = Product