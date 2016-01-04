# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class MayTinhThienMinhSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['maytinhthienminh.vn']
    start_urls = [
        'http://maytinhthienminh.vn/laptop_dm663.html#.VoT1X3V97VM',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://maytinhthienminh.vn/laptop_dm663.html\&page=[0-9]+'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="productName"]/a[1]/@href',
        'source' : 'maytinhthienminh.vn',
        'title' : '//*[@id="product_name"]//text()',
        'price' : '//*[@class="p_price" or @class="price_info"]//span[@class="price"]//text()'
    }