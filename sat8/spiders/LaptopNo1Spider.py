# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class LaptopNo1Spider(AbstractPriceSpider):

    allowed_domains = ['laptopno1.com']
    start_urls = [
        'http://laptopno1.com/tim-kiem-san-pham/-/-1/1.htm',
    ]

    rules = (

    )

    configs = {
        'product_links' : '//*[@class="item-sp"]//a[1]/@href',
        'source' : 'laptopno1.com',
        'title' : '//*[@class="detail-left"]/h1/text()',
        'price' : '//*[@class="detail-right"]//p[@class="giaban"]//text() | //*[@class="detail-right"]//span[2]/text()'
    }