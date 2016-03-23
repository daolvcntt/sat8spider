# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class ItshophanoiSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['itshophanoi.vn']
    start_urls = [
        'http://itshophanoi.vn/shops/LAPTOP.html',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://itshophanoi.vn/shops/LAPTOP/page-[0-9]+.html'), restrict_xpaths=('//div[@class="pages"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="products"]//a[1]/@href',
        'source' : 'itshophanoi.vn',
        'title' : '//*[@class="title_productdetail"]/h1//text()',
        'price' : '//*[@class="price_box_productdetail"]//span[1]//text()'
    }