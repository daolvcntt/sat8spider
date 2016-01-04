# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class VinhPhatMobileSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['vinhphatmobile.com']
    start_urls = [
        'http://vinhphatmobile.com/dien-thoai/',
        'http://vinhphatmobile.com/macbook/',
        'http://vinhphatmobile.com/may-tinh-bang/'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://vinhphatmobile.com/dien-thoai/page\-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination__items"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@id="category_products_11"]//a[@class="product-title"]/@href',
        'source' : 'vinhphatmobile.com',
        'title' : '//*[@class="ty-product-bigpicture__left-wrapper"]//h1/text()',
        'price' : '//*[@class="ty-product-block__price-actual"]//span[@class="ty-price-num"]/text()'
    }