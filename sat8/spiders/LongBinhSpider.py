# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class LongBinhSpider(AbstractPriceSpider):
    allowed_domains = ['longbinh.com.vn']
    start_urls = [
        'http://longbinh.com.vn/laptop/',
        'http://longbinh.com.vn/may-tinh-bang/',
        'http://longbinh.com.vn/dien-thoai/'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://longbinh.com.vn/laptop/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://longbinh.com.vn/may-tinh-bang/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://longbinh.com.vn/dien-thoai/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="grid-list"]//a[1]/@href',
        'source' : 'longbinh.com.vn',
        'title' : '//*[@class="ty-product-block-title"]/text()',
        'price' : '//*[@class="ty-price"]//text()'
    }