# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class AppleproSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['www.applepro.vn']
    start_urls = [
        'http://www.applepro.vn/iphone-6-plus',
        'http://www.applepro.vn/iphone-6s',
        'http://www.applepro.vn/iphone-6s-plus',
        'http://www.applepro.vn/ipad-mini',
        'http://www.applepro.vn/ipad-mini-3',
        'http://www.applepro.vn/ipad-mini-4',
        'http://www.applepro.vn/ipad-air-2',
        'http://www.applepro.vn/macbook',
        'http://www.applepro.vn/imac',
        'http://www.applepro.vn/mac-mini'
    ]

    rules = (

    )

    configs = {
        'product_links' : '//*[@class="item-product"]/a[@class="hover"]/@href',
        'source' : 'www.applepro.vn',
        'title' : '//*[@class="body-detail"]/h1//text()',
        'price' : '//*[@class="body-detail"]/strong[1]/text()'

    }