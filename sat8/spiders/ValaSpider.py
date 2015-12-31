# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class ValaSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['vala.vn']
    start_urls = [
        'https://vala.vn/danh-sach-san-pham/-/catalog/laptop-640',
        'https://vala.vn/danh-sach-san-pham/-/catalog/dien-thoai-di-do-1-596',
        'https://vala.vn/danh-sach-san-pham/-/catalog/tablet-may-tinh-bang--602'
    ]

    rules = (
        Rule (LinkExtractor(allow=('https://vala.vn/danh-sach-san-pham/-/catalog/laptop-640\?cur=[0-9]+'), restrict_xpaths=('//div[@class="catalog-box-bottom"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('https://vala.vn/danh-sach-san-pham/-/catalog/dien-thoai-di-do-1-596\?cur=[0-9]+'), restrict_xpaths=('//div[@class="catalog-box-bottom"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('https://vala.vn/danh-sach-san-pham/-/catalog/tablet-may-tinh-bang--602\?cur=[0-9]+'), restrict_xpaths=('//div[@class="catalog-box-bottom"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product-name"]/a[1]/@href',
        'source' : 'vala.vn',
        'title' : '//*[@class="prd-title"]/text()',
        'price' : '//*[@id="valuePrice"]/text()'
    }