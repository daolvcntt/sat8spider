# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class BestStoreSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['beststore.vn']
    start_urls = [
        'http://beststore.vn/san-pham/135/may-tinh-xach-tay/',
        'http://beststore.vn/san-pham/134/may-tinh-bang/',
        'http://beststore.vn/san-pham/138/dien-thoai/'
    ]

    rules = ()

    configs = {
        'product_links' : '//*[@class="item-products"]//a[1]/@href',
        'source' : 'beststore.vn',
        'title' : '//*[@class="title_product"]/text()',
        'price' : '//*[@class="wrap_rice"]//div[@class="rice"]/text()'
    }

    def parse(self, response):
        return self.parse_item(response)