# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class ThanhNamPcSpider(AbstractPriceSpider):

    allowed_domains = ['thanhnampc.vn']

    start_urls = [
        'http://thanhnampc.vn/ls/may-tinh-xach-tay-c360.html',
        'http://thanhnampc.vn/ls/may-tinh-bang-c366.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('may-tinh-xach-tay-c360-page\-[0-9]+.html'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="middle listpro"]//li[@class="lli"]//a[@class="lmhref"]/@href',
        'source' : 'thanhnampc.vn',
        'title' : '//*[@class="ptitle"]/h1/text()',
        'price' : '//*[@class="pprice"]/span[@class="price"]/text()'
    }