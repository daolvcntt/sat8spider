# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class MnMobileSpider(AbstractPriceSpider):
    allowed_domains = ['www.mnmobile.vn', ]

    start_urls = [
        'http://www.mnmobile.vn/vn/san-pham/dien-thoai-1.html',
        'http://www.mnmobile.vn/vn/san-pham/may-tinh-bang-2.html'
    ]

    configs = {
        'product_links' : '//*[@class="boxItem"]//td/a/@href',
        'source' : 'www.mnmobile.vn',
        'title' : '//*[@class="titleL"]/h1/text()',
        'price' : '//*[@class="prod_dt_price"]/span/text() | //*[@id="divInfo"]//div[@class="price_old"]/span/text()'
    }

    def parse(self, response):
        return self.parse_item(response)