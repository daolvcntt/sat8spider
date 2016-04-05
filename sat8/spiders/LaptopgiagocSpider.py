# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class LaptopgiagocSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['laptopgiagoc.vn']
    start_urls = [
        'http://laptopgiagoc.vn/san-pham',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://laptopgiagoc.vn/san-pham\?page=[0-9]+'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="pricelist"]//a[@class="tdname"]/@href',
        'source' : 'laptopgiagoc.vn',
        'title' : '//*[@class="product-info"]/h1//text()',
        'price' : '//*[@class="thongtinsp-content"]//span[@class="price-new"]//text()'
    }