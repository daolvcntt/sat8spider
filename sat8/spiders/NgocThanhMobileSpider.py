# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class NgocThanhMobileSpider(AbstractPriceSpider):
    allowed_domains = ['ngocthanhmobile.com']
    start_urls = [
        'http://ngocthanhmobile.com/home/chungloai/3/1/Dien_thoai',
        'http://ngocthanhmobile.com/home/chungloai/1/1/Apple'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://ngocthanhmobile.com/home/chungloai/3/[0-9]+/'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://ngocthanhmobile.com/home/chungloai/1/[0-9]+/'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="hinhspnew"]//a[1]/@href',
        'source' : 'ngocthanhmobile.com',
        'title' : '//*[@id="motachitiet"]//p[1]//text()',
        'price' : '//*[@class="lineheight"]//span[2]//text()'
    }