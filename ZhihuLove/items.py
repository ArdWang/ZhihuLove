# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuloveItem(scrapy.Item):
    # 用户名
    username = scrapy.Field()

    # 用户介绍
    introduce = scrapy.Field()

    # 用户内容
    content = scrapy.Field()



