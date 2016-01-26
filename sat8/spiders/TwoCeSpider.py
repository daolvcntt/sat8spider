# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class TwoCeSpider(AbstractPriceSpider):

    allowed_domains = ['2ce.com.vn']
    start_urls = [
        'http://2ce.com.vn/danh-sach/laptop/376.html',
        'http://2ce.com.vn/danh-sach/may-tinh-bang/377.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('danh-sach/laptop/376.html\&p\=[0-9]+')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product_list"]//a[@class="img_product"]/@href',
        'source' : '2ce.com.vn',
        'title' : '//*[@class="product-basic-info"]//h3[1]/text()',
        'price' : '//*[@class="product-basic-info"]//div[@class="red"]//text()'
    }