# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from atlas.models import Product, Review


# class ProductItem(scrapy.Item):
class ProductItem(DjangoItem):
    django_model = Product  # for DjangoItem


class ReviewItem(DjangoItem):
    django_model = Review  # for DjangoItem
