# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class LaptopGiaHuySpider(AbstractPriceSpider):
    allowed_domains = ['laptopgiahuy.vn']
    start_urls = [
        'http://laptopgiahuy.vn/dien-thoai-di-dong-pi=1.html',
        'http://laptopgiahuy.vn/may-tinh-bang-pi=1.html'
    ]

    rules = (
    )

    configs = {
        'product_links' : '//*[@class="Home-Product text-center col-xs-12 col-sm-6 col-md-4 col-lg-3"]/@href',
        'source' : 'laptopgiahuy.vn',
        'title' : '//*[@class="ProductNameLink ProductNameLinkDetail"]//text()',
        'price' : '//*[@class="ProductPriceNew clearfix"]//text()'
    }

    def __init__(self):
        for i in range(1, 5):
            url = 'http://laptopgiahuy.vn/dien-thoai-di-dong-pi=' + str(i) + '.html'
            self.start_urls.append(url)

        for i in range(1, 8):
            url = 'http://laptopgiahuy.vn/may-tinh-bang-pi=' + str(i) + '.html'
            self.start_urls.append(url)


    def parse(self, response):
        return self.parse_item(response)