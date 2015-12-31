# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class HuyHoangSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['huyhoang.vn']
    start_urls = [
        'http://huyhoang.vn/laptop',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://huyhoang.vn/laptop\?p=[0-9]+'), restrict_xpaths=('//div[@class="page-number"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="box-td"]/a[1]/@href',
        'source' : 'huyhoang.vn',
        'title' : '//*[@class="content-main"]//h1[1]//text()',
        'price' : '//*[@class="price-new"]//text()'
    }