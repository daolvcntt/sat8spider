# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class AchauMobileSpider(AbstractPriceSpider):
    allowed_domains = ['achaumobile.com']

    start_urls = [
        'http://achaumobile.com/dien-thoai/iphone-6--6-plus.php',
        'http://achaumobile.com/dien-thoai/iphone-6s--6s-plus.php',
        'http://achaumobile.com/dien-thoai/iphone-5-5s.php',
        'http://achaumobile.com/dien-thoai/samsung.php',
        'http://achaumobile.com/may-tinh-bang/ipad-mini-2---3---4.php',
        'http://achaumobile.com/may-tinh-bang/ipad-air.php',
        'http://achaumobile.com/may-tinh-bang/ipad-air-2.php',
        'http://achaumobile.com/may-tinh-bang/ipad-mini-3.php',
        'http://achaumobile.com/may-tinh-bang/ipad-mini-4.php',
        'http://achaumobile.com/may-tinh-bang/ipad-pro.php'
    ]

    rules = (

    )

    configs = {
        'product_links' : '//*[@class="pitem"]//a[1]/@href',
        'source' : 'achaumobile.com',
        'title' : '//*[@class="PTitle"]//h1//text()',
        'price' : '//*[@class="MdetailPri"]/a//text()'
    }

    def parse(self, response):
        return self.parse_item(response);