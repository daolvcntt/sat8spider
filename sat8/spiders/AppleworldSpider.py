# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class AppleworldSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['appleworld.vn']
    start_urls = [
        'http://appleworld.vn/vi/spds/id180/IPad-Mini-3/',
        'http://appleworld.vn/vi/spds/id197/iPad-Mini-4/',
        'http://appleworld.vn/vi/spds/id181/IPad-Air-2/',
        'http://appleworld.vn/vi/spds/id196/IPad-Pro/',
        'http://appleworld.vn/vi/spds/id177/IPhone-6---6S/',
        'http://appleworld.vn/vi/spds/id178/Iphone-6-Plus---6S-Plus/',
        'http://appleworld.vn/vi/spds/id111/IPod/',
        'http://appleworld.vn/vi/spds/id191/Macbook-12/',
        'http://appleworld.vn/vi/spds/id106/MacBookAir/',
        'http://appleworld.vn/vi/spds/id103/MacBookPro/',
        'http://appleworld.vn/vi/spds/id145/Mac-Mini/',
        'http://appleworld.vn/vi/spds/id115/IMac/'
    ]

    rules = (
        # Rule (LinkExtractor(allow=('https://appleworld.vn/dien-thoai-smartphone/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="item-top-title"]/a/@href',
        'source' : 'appleworld.vn',
        'title' : '//*[@class="tensp"]/a/text()',
        'price' : '//*[@class="gia"]//text()'
    }