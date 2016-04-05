# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class NamaSpider(AbstractPriceSpider):
    allowed_domains = ['nama.com.vn']
    start_urls = [
        'http://nama.com.vn/iphone-p2.html',
        'http://nama.com.vn/ipad-p3.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://nama.com.vn/iphone-p2.html-trang-[0-9]+'), restrict_xpaths=('//div[@class="db_tabPr"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://nama.com.vn/ipad-p3.html-trang-[0-9]+'), restrict_xpaths=('//div[@class="db_tabPr"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="prl_img"]/@href',
        'source' : 'nama.com.vn',
        'title' : '//*[@class="pdt_tt"]/h1//text()',
        'price' : '//*[@class="pdt_gia"]//font[1]//text()'
    }