# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class TuNguyetSpider(AbstractPriceSpider):
    allowed_domains = ['tunguyet.vn']
    start_urls = [
        'http://tunguyet.vn/Products.aspx?DepartmentID=45',
        'http://tunguyet.vn/Products.aspx?DepartmentID=46',
    ]

    rules = ()

    configs = {
        'product_links' : '//*[@class="cssImg"]//a[1]/@href',
        'source' : 'tunguyet.vn',
        'title' : '//*[@class="proDetail"]/text()',
        'price' : '//*[@class="proDetail-price"]//text()'
    }

    def parse(self, response):
        return self.parse_item(response)