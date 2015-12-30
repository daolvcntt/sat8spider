# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class TgddLaptopTabletPriceSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ["thegioididong.com"]

    start_urls = [
        'https://www.thegioididong.com/laptop?trang=1',
        'https://www.thegioididong.com/may-tinh-bang?trang=1'
    ]

    rules = (
        Rule (LinkExtractor(allow=('laptop\?trang\=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('may-tinh-bang\?trang\=[0-9]+')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@id="lstprods"]/li/a[1]/@href',
        'source' : 'thegioididong.com',
        'title' : '//*[@class="rowtop"]/h1//text()',
        'price' : '//*[@class="price_sale"]/strong[1]/text()'
    }