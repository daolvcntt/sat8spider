# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class LaptopVipSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['www.laptopvip.vn']
    start_urls = [
        'https://www.laptopvip.vn/hang-san-xuat.html',
        'https://www.laptopvip.vn/dien-thoai.html',
        'https://www.laptopvip.vn/hang-san-xuat-vi.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('https://www.laptopvip.vn/hang-san-xuat-page\-[0-9]+.html'), restrict_xpaths=('//div[@class="ty-pagination__bottom"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="title-price-wrapper"]/a[@class="product-title"]/@href',
        'source' : 'www.laptopvip.vn',
        'title' : '//*[@class="info-left"]//h1[@class="ty-mainbox-title"]/text()',
        'price' : '//*[@class="actual-price"]//span[@class="ty-price-num"]/text()'
    }