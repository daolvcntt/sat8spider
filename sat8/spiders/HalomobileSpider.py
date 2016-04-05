# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class HalomobileSpider(AbstractPriceSpider):
    allowed_domains = ['halomobile.vn']
    start_urls = [
        'http://halomobile.vn/dien-thoai.html',
        'http://halomobile.vn/may-tinh-bang.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://halomobile.vn/dien-thoai.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="row pagination"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://halomobile.vn/may-tinh-bang.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="row pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product-details"]//a[1]/@href',
        'source' : 'halomobile.vn',
        'title' : '//*[@class="heading-title"]//text()',
        'price' : '//*[@class="product-price"]//text()'
    }