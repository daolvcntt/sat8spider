# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class MaytinhBachGiaSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['maytinhbachgia.vn']
    start_urls = [
        'http://maytinhbachgia.vn/msi',
        'http://maytinhbachgia.vn/DELL',
        'http://maytinhbachgia.vn/ASUS',
        'http://maytinhbachgia.vn/HP',
        'http://maytinhbachgia.vn/lenovo'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://maytinhbachgia.vn/msi\?page=[0-9]+'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://maytinhbachgia.vn/DELL\?page=[0-9]+'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://maytinhbachgia.vn/ASUS\?page=[0-9]+'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="pro-list"]//a[1]/@href',
        'source' : 'maytinhbachgia.vn',
        'title' : '//*[@class="main-title"]/text()',
        'price' : '//*[@class="line-price clearfix"]/p[@class="price"]/text()'
    }