# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class BinhNguyenCbSpider(AbstractPriceSpider):
    allowed_domains = ['binhnguyencb.com']
    start_urls = [
        'http://binhnguyencb.com/dien-thoai/388333.html',
    ]

    rules = (
        Rule (LinkExtractor(allow=('dien-thoai/388333.html\?pn=[0-9]+'), restrict_xpaths=('//div[@class="PageNavigation"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="ProductImage ProductImageTooltip"]/a[1]/@href',
        'source' : 'binhnguyencb.com',
        'title' : '//*[@class="product-title"]/h1//text()',
        'price' : '//*[@class="ProductPrice VariationProductPrice"]//text()'
    }