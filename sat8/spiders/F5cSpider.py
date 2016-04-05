# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class F5cSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['f5c.vn']
    start_urls = [
        'http://f5c.vn/laptop.html',
        'http://f5c.vn/smartphone.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://f5c.vn/laptop.html\?cat=11\&display_type=0\&per_page=[0-9]+'), restrict_xpaths=('//ul[@class="pagination"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://f5c.vn/smartphone.html\?cat=406\&display_type=0\&per_page=[0-9]+'), restrict_xpaths=('//ul[@class="pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@id="widget_product_list"]//a[@class="name-product"]/@href',
        'source' : 'f5c.vn',
        'title' : '//*[@class="entry-detail"]/h1//text()',
        'price' : '//*[@class="entry-detail"]//span[@class="price_new"]//text()'
    }