# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DienMayManhCuongSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ["dienmaymanhcuong.com"]

    start_urls = [
        'http://dienmaymanhcuong.com/may-tinh-8517/',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://dienmaymanhcuong.com/page/may-tinh-8517/p\/[0-9]+/')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="frame_img_dm"]//a[1]/@href',
        'source' : 'dienmaymanhcuong.com',
        'title' : '//*[@class="name-item"]//h2[1]//text()',
        'price' : '//*[@class="price-item"]//h2[1]/text()'
    }