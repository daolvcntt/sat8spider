# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class ChonhapkhauSpider(AbstractPriceSpider):
    allowed_domains = ['chonhapkhau.com']
    start_urls = [
        'http://chonhapkhau.com/may-tinh-dien-thoai-di-dong-tp21',
    ]

    rules = (
    )

    configs = {
        'product_links' : '//*[@class="product-item"]//a[1]/@href',
        'source' : 'chonhapkhau.com',
        'title' : '//*[@class="title"]//text()',
        'price' : '//*[@class="price-current"]//text()'
    }

    def parse(self, response):
        return self.parse_item(response);