# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class StyleMobileSpider(AbstractPriceSpider):
    allowed_domains = ['stylemobile.vn']
    start_urls = [
        'http://stylemobile.vn/c52760/apple',
        'http://stylemobile.vn/c52774/samsung',
        'http://stylemobile.vn/c52768/sony',
        'http://stylemobile.vn/c52780/htc',
        'http://stylemobile.vn/c52783/blackberry',
        'http://stylemobile.vn/c52784/lg',
        'http://stylemobile.vn/c52785/asus',
        'http://stylemobile.vn/c52786/vertu'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://stylemobile.vn/c52760/apple\?page=[0-9]+'), restrict_xpaths=('//div[@class="paginator"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://stylemobile.vn/c52774/samsung\?page=[0-9]+'), restrict_xpaths=('//div[@class="paginator"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="col-md-8 col-sm-8 col-xs-24"]//a[1]/@href',
        'source' : 'stylemobile.vn',
        'title' : '//*[@id="product-main"]/h1//text()',
        'price' : '//*[@class="price"]//text()'
    }