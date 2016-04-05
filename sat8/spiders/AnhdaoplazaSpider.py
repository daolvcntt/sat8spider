# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class AnhdaoplazaSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['anhdaoplaza.vn']
    start_urls = [
        'http://anhdaoplaza.vn/collections/all',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://anhdaoplaza.vn/collections/all\?page=[0-9]+'), restrict_xpaths=('//ul[@class="pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="products-grid"]//a[@class="product-image"]/@href',
        'source' : 'anhdaoplaza.vn',
        'title' : '//*[@class="product-essential"]//div[@class="product-name"]/h1//text()',
        'price' : '//*[@class="special-price"]//text()'
    }