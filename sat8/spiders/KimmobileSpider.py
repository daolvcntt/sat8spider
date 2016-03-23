# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class KimmobileSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['www.kimmobile.com']
    start_urls = [
        'http://www.kimmobile.com/dien-thoai',
        'http://www.kimmobile.com/may-tinh-bang'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://www.kimmobile.com/dien-thoai\?page=[0-9]+'), restrict_xpaths=('//div[@class="page_break"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="page_content_prodcut"]//div[@class="product_picture"]/a/@href',
        'source' : 'www.kimmobile.com',
        'title' : '//*[@class="content_left"]//h1[@class="page_title"]//text()',
        'price' : '//*[@class="price-not-bhv"]//text()'
    }