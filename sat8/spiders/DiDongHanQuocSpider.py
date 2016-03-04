# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DiDongHanQuocSpider(AbstractPriceSpider):
    allowed_domains = ['www.didonghanquoc.com']
    start_urls = [
        'http://www.didonghanquoc.com/dien-thoai',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://www.didonghanquoc.com/dien-thoai?page=[0-9]+'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="a_pro"]/@href',
        'source' : 'www.didonghanquoc.com',
        'title' : '//*[@class="product-infos"]//h1//text()',
        'price' : '//*[@class="price-gia"]//text()'
    }