# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DigiPhoneSpider(AbstractPriceSpider):
    allowed_domains = ['digiphone.com.vn', ]

    start_urls = [
        'http://digiphone.com.vn/dien-thoai/',
        'http://digiphone.com.vn/may-tinh-bang/'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://digiphone.com.vn/dien-thoai/\&p=[0-9]'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="xemchitiet_sp"]/@href',
        'source' : 'digiphone.com.vn',
        'title' : '//*[@class="name_product"]/text()',
        'price' : '//*[@class="giagiam"]/text()'
    }

    def start_requests(self):
        request = []

        for i in range(1,6):
            request.append(scrapy.Request('http://www.hnammobile.com/dien-thoai/?p=%s#ds' % i, callback=self.parse_item))

        request.append(scrapy.Request('http://www.hnammobile.com/may-tinh-bang/', callback=self.parse_item))
        request.append(scrapy.Request('http://www.hnammobile.com/laptop/apple.html', callback=self.parse_item))