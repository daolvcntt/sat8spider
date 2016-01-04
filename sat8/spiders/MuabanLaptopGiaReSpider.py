# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class MuabanLaptopGiaReSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ["muabanlaptopcu.vn"]

    start_urls = [
        'http://muabanlaptopcu.vn/laptop-gia-re'
    ]

    configs = {
        'product_links' : '//*[@class="product-block"]/div/a[1]/@href',
        'source' : 'muabanlaptopcu.vn',
        'title' : '//*[@class="product-info"]//h1//text()',
        'price' : '//*[@class="price-gruop"]//text()'
    }

    def parse(self, reponse):
        return self.parse_item(reponse)