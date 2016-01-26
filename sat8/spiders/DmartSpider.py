# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DmartSpider(AbstractPriceSpider):

    allowed_domains = ['www.dmart.vn']
    start_urls = [
        'http://www.dmart.vn/maytinhlaptop/Laptop-p1169.html',
        'http://www.dmart.vn/maytinhlaptop/Dien-thoai-May-tinh-bang-p1238.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('/maytinhlaptop/type\.php\?module=product\&iCat=1169\&page=[0-9]+'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('/maytinhlaptop/type\.php\?module=product\&iCat=1238\&page=[0-9]+'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="tableproduct"]//div[@class="name"]/a[1]/@href',
        'source' : 'www.dmart.vn',
        'title' : '//*[@id="contentframe"]//h1[@class="ptitle"]//text()',
        'price' : '//*[@class="listdetail"][3]//text() | //*[@class="listdetail"][1]//text()'
    }