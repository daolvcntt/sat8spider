# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class NmobileSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['nmobile.vn']
    start_urls = [
        'http://nmobile.vn/dien-thoai.htm',
        'http://nmobile.vn/may-tinh-bang.htm'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://nmobile.vn/dien-thoai.htm\&p=[0-9]+'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="img_sp"]//a[1]/@href',
        'source' : 'nmobile.vn',
        'title' : '//*[@class="chitietthongtinsp"]//h2[1]/text()',
        'price' : '//*[@class="giabandetail"]/text()'
    }