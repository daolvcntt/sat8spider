# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DienThoaiSaiGonSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['dienthoaisaigon.com']
    start_urls = [
        'http://www.dienthoaisaigon.com/r/dienthoai/',
        'http://www.dienthoaisaigon.com/r/maytinhbang/'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://www.dienthoaisaigon.com/r/dienthoai/page/[0-9]+')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@id="ul-product"]/li/a[1]/@href',
        'source' : 'dienthoaisaigon.com',
        'title' : '//*[@class="product_title entry-title"]//text()',
        'price' : '//*[@class="price"]/span[1]//text()'
    }