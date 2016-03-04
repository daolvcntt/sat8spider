# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class ViettabletSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['www.viettablet.com']
    start_urls = [

    ]

    rules = ()

    configs = {
        'product_links' : '//*[@class="a_img_highlight"]/@href',
        'source' : 'www.viettablet.com',
        'title' : '//*[@class="tit_single"]//text()',
        'price' : '//*[@class="new_price_sg"]//text()'
    }

    def __init__(self):
        for i in range(1, 51):
            url = 'http://www.viettablet.com/index.php?route=module/ajax/pagi&category=80&page=' + str(i)
            self.start_urls.append(url)


    def parse(self, response):
        return self.parse_item(response)
