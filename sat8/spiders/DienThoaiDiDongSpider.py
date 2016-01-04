# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DienThoaiDiDongSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['www.dienthoaididong.com']
    start_urls = [
        # phone
        'https://www.dienthoaididong.com/ajax/Group/ViewMoreProduct?intMainGroupId=1&brandid=-1&strOs=&strPriceRange=-1&strOrder=&intNumProd=200&pageindex=1&_=1451705506653',
        'https://www.dienthoaididong.com/ajax/Group/ViewMoreProduct?intMainGroupId=1&brandid=-1&strOs=&strPriceRange=-1&strOrder=&intNumProd=200&pageindex=2&_=1451705506653',
        'https://www.dienthoaididong.com/ajax/Group/ViewMoreProduct?intMainGroupId=1&brandid=-1&strOs=&strPriceRange=-1&strOrder=&intNumProd=200&pageindex=3&_=1451705506653',
        # tablet
        'https://www.dienthoaididong.com/ajax/Group/ViewMoreProduct?intMainGroupId=2&brandid=-1&strOs=&strPriceRange=-1&strOrder=&intNumProd=500&pageindex=1&_=1451705813783'
    ]

    rules = ()

    configs = {
        'product_links' : '//li/a/@href',
        'source' : 'www.dienthoaididong.com',
        'title' : '//*[@class="detailCont"]//h1[@class="title"]//text()',
        'price' : '//*[@class="detailInfo"]//div[@class="price"]/text()'
    }

    def parse(self, response):
        return self.parse_item(response)