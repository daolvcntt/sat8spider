# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class AnKhangSpider(AbstractPriceSpider):
    allowed_domains = ["www.ankhang.vn"]

    start_urls = [
        'http://www.ankhang.vn/may-tinh-xach-tay_dm167.html?page=1',
    ]

    rules = (
        Rule (LinkExtractor(allow=('may-tinh-xach-tay_dm167.html\?page=[0-9]+')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="p_container"]//a[@class="p_name"]/@href',
        'source' : 'www.ankhang.vn',
        'title' : '//*[@id="overview"]/h1/text()',
        'price' : '//*[@id="price_detail"]/div[@class="img_price_full"]/text()'
    }