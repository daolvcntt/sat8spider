# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class NovaComVnSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ["www.nova.com.vn"]

    start_urls = [
        'http://www.nova.com.vn/chuyen-muc-may-tinh-bang--laptop/laptop/1/1',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://www.nova.com.vn/chuyen-muc-may-tinh-bang--laptop/laptop/1\/[0-9]+')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product-image"]//a[1]/@href',
        'source' : 'www.nova.com.vn',
        'title' : '//*[@class="product-single"]//h2//text()',
        'price' : '//*[@class="product-single"]//span[@class="price"]/text()'
    }