# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class AmazonVnSpider(AbstractPriceSpider):
    allowed_domains = ['amazona.vn']
    start_urls = [
        'http://amazona.vn/danh-muc/may-tinh-xach-tay-laptop.html',
        'http://amazona.vn/danh-muc/tablet-may-tinh-bang.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://amazona.vn/danh-muc/may-tinh-xach-tay-laptop.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="navigation"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://amazona.vn/danh-muc/tablet-may-tinh-bang.html')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="img_product"]/a/@href',
        'source' : 'amazona.vn',
        'title' : '//*[@class="info_detail_P"]/h1[@class="h1Title"]/text()',
        'price' : '//*[@class="dt_price"]/text()'
    }