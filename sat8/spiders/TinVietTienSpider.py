# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class TinVietTienSpider(AbstractPriceSpider):

    allowed_domains = ['tinviettien.vn']
    start_urls = [
        'http://tinviettien.vn/laptop/san-pham-moi.htm',
        'http://tinviettien.vn/laptop/san-pham-giam-gia.htm',
        'http://tinviettien.vn/laptop/san-pham-ban-chay.htm',
        'http://tinviettien.vn/may-tinh-bang/san-pham-moi.htm',
        'http://tinviettien.vn/may-tinh-bang/san-pham-giam-gia.htm',
        'http://tinviettien.vn/may-tinh-bang/san-pham-khuyen-mai.htm',
        'http://tinviettien.vn/may-tinh-bang/san-pham-ban-chay.htm'
    ]

    rules = (
    )

    configs = {
        'product_links' : '//*[@class="product-list"]//a[1]/@href',
        'source' : 'tinviettien.vn',
        'title' : '//*[@class="pro_name"]/text()',
        'price' : '//*[@class="price_value"]/text()'
    }