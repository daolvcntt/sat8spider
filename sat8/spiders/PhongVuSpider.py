# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class PhongVuSpider(AbstractPriceSpider):
    allowed_domains = ["phongvu.vn"]
    start_urls = [
        'http://phongvu.vn/may-tinh/may-tinh-xach-tay-laptop-1670c.html',
        'http://phongvu.vn/dien-thoai/dien-thoai-di-dong-1192c.html',
        'http://phongvu.vn/san-pham-apple/iphone-1676c.html',
        'http://phongvu.vn/san-pham-apple/ipad-1675c.html'
    ]
    rules = (
        Rule (LinkExtractor(allow=('http://phongvu.vn/may-tinh/may-tinh-xach-tay-laptop-1670/cpage\-[0-9]+\.html')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://phongvu.vn/dien-thoai/dien-thoai-di-dong-1192/cpage\-[0-9]+\.html')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://phongvu.vn/san-pham-apple/iphone-1676c/cpage\-[0-9]+\.html')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="picsp"]/a[1]/@href',
        'source' : 'phongvu.vn',
        'title' : '//*[@class="chitietsp"]/h1/text()',
        'price' : '//*[@class="giasp"]/text()'
    }