# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class IsSmartPhoneSpider(AbstractPriceSpider):
    allowed_domains = ['www.ismartphone.vn', 'www.ismartphone.vn']
    start_urls = [
        'http://www.ismartphone.vn/dien-thoai.html',
        'http://www.ismartphone.vn/may-tinh-bang.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://www.ismartphone.vn/dien-thoai-page-[0-9]+.html'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="cm-gallery-item cm-item-gallery"]/a/@href',
        'source' : 'www.ismartphone.vn',
        'title' : '//*[@class="mainbox-title"]/text()',
        'price' : '//*[@class="price"]/span[1]/text()'
    }