# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class MaiMuaSpider(AbstractPriceSpider):
    allowed_domains = ['maimua.com']
    start_urls = [
        'http://maimua.com/th-laptop',
        'http://maimua.com/Smartphone',
        'http://maimua.com/may-tinh-bang'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://maimua.com/th-laptop\?page=[0-9]+'), restrict_xpaths=('//div[@class="links"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://maimua.com/Smartphone\?page=[0-9]+'), restrict_xpaths=('//div[@class="links"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://maimua.com/may-tinh-bang\?page=[0-9]+'), restrict_xpaths=('//div[@class="links"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product-meta"]//a[1]/@href',
        'source' : 'maimua.com',
        'title' : '//*[@class="product-info"]//h1[@class="title-produt-"]/text()',
        'price' : '//*[@class="price-new"]/text()'
    }