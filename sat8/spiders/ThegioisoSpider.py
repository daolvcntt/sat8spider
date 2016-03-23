# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class ThegioisoSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['thegioiso.vn']
    start_urls = [
        'http://thegioiso.vn/laptop-296.html',
        'http://thegioiso.vn/dien-thoai-472.html',
        'http://thegioiso.vn/tablet-498.html',
        'http://thegioiso.vn/apple--521.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://thegioiso.vn/laptop-296.html&page=[0-9]+'), restrict_xpaths=('//center[@class="pageview clearfix"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://thegioiso.vn/dien-thoai-472.html&page=[0-9]+'), restrict_xpaths=('//center[@class="pageview clearfix"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://thegioiso.vn/tablet-498.html&page=[0-9]+'), restrict_xpaths=('//center[@class="pageview clearfix"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://thegioiso.vn/apple--521.html&page=[0-9]+'), restrict_xpaths=('//center[@class="pageview clearfix"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product-group"]//a/@href',
        'source' : 'thegioiso.vn',
        'title' : '//*[@class="panel-heading"]/span//text()',
        'price' : '//*[@class="price-sale"]//text()'
    }