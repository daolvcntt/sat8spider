# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class ZshopSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['zshop.vn']
    start_urls = [
        'https://zshop.vn/dien-thoai-smartphone/',
        'https://zshop.vn/may-tinh-bang/',
        'https://zshop.vn/macbook/',
        'https://zshop.vn/iphone/',
        'https://zshop.vn/ipad-cu/'
        'https://zshop.vn/macbook-cu/',
        'https://zshop.vn/laptop-cu/',

        'https://zshop.vn/iphone-cu/',
        'https://zshop.vn/ipad/',
    ]

    rules = (
        Rule (LinkExtractor(allow=('https://zshop.vn/dien-thoai-smartphone/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('https://zshop.vn/may-tinh-bang/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('https://zshop.vn/macbook/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('https://zshop.vn/iphone/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('https://zshop.vn/ipad-cu/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('https://zshop.vn/macbook-cu/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('https://zshop.vn/laptop-cu/page-[0-9]+/'), restrict_xpaths=('//div[@class="ty-pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="ty-grid-list__image"]/a/@href',
        'source' : 'zshop.vn',
        'title' : '//*[@class="ty-product-block-title"]/text()',
        'price' : '//*[@class="ty-product-block__price-actual"]//span[@class="ty-price"]//text()'
    }