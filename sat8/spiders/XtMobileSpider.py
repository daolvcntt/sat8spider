# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class XtMobileSpider(AbstractPriceSpider):
    allowed_domains = ['xtmobile.vn']
    start_urls = [
        'http://xtmobile.vn/dien-thoai',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://xtmobile.vn/dien-thoai/p\-[0-9]+,sort-0'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="boxItem"]//a[1]/@href',
        'source' : 'xtmobile.vn',
        'title' : '//*[@class="titleL"]/h1//text()',
        'price' : '//*[@id="price"]//text()'
    }