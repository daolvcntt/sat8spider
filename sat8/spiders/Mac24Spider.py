# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class Mac24Spider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['mac24h.vn']
    start_urls = [
        'http://mac24h.vn/mac/'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://mac24h.vn/mac/page\-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="ty-grid-list__item-name"]//a[1]/@href',
        'source' : 'mac24h.vn',
        'title' : '//*[@class="ty-product-block-title"]/text()',
        'price' : '//*[@class="ty-price"]/span[@class="ty-price-num"]/text()'
    }