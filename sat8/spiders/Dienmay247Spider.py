# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class Dienmay247Spider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['www.dienmay247.com']
    start_urls = [
        'http://www.dienmay247.com/may-vi-tinh-and-laptop/laptop/',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://www.dienmay247.com/may-vi-tinh-and-laptop/laptop/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="grid-list"]//a[@class="product-title"]/@href',
        'source' : 'www.dienmay247.com',
        'title' : '//*[@class="ty-product-block-title"]//text()',
        'price' : '//*[@class="ty-price-num"]//text()'
    }
