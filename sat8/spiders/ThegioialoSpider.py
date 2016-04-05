# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class ThegioialoSpider(AbstractPriceSpider):
    allowed_domains = ['www.thegioialo.com.vn']
    start_urls = [
        'http://www.thegioialo.com.vn/san-pham/dien-thoai-iphone-2.html',
        'http://www.thegioialo.com.vn/san-pham/may-tinh-bang-3.html'
    ]

    rules = (

    )

    configs = {
        'product_links' : '//*[@class="boxItem"]//a[1]/@href',
        'source' : 'www.thegioialo.com.vn',
        'title' : '//*[@class="titleL"]/h1//text()',
        'price' : '//*[@class="div_price"]//text()'
    }

    def parse(self, response):
        return self.parse_item(response)