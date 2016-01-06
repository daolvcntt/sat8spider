# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class HongHaAsiaSpider(AbstractPriceSpider):
    allowed_domains = ['hongha.asia']
    start_urls = [
        'http://hongha.asia/cat/17.html',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://hongha.asia/cat/17/page[0-9]+.html')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="ProTitle"]//a[1]/@href',
        'source' : 'hongha.asia',
        'title' : '//*[@id="namepro"]/text()',
        'price' : '//*[@id="overviewpro"]//tr//div[@class="giasanpham"][2]/text()'
    }