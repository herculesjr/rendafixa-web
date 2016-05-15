# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    last_update = scrapy.Field()


class BoundItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    date = scrapy.Field()
    sell_tax = scrapy.Field()
    sell_price = scrapy.Field()
    buy_tax = scrapy.Field()
    buy_price = scrapy.Field()
