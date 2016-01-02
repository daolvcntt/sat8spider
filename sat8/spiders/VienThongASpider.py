# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class VienThongASpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['www.vienthonga.vn']
    start_urls = [
        # phone
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152535&page=1',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152535&page=2',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152535&page=3',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152535&page=4',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152535&page=5',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152535&page=6',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152535&page=7',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152535&page=8',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152535&page=9',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152535&page=10',

       # table
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=171730&page=1',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=171730&page=2',

       # laptop
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152537&page=1',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152537&page=2',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152537&page=3',
       'https://www.vienthonga.vn/Category/LoadMoreCate?cateid=152537&page=4',
    ]

    rules = ()

    configs = {
        'product_links' : '//*[@class="product-image"]/a[1]/@href',
        'source' : 'www.vienthonga.vn',
        'title' : '//*[@class="detail-header"]//h1[@class="name"]/text()',
        'price' : '//*[@class="detail-price"]/text()'
    }

    def parse(self, response):
        return self.parse_item(response)