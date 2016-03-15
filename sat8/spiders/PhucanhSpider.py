# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class PhucanhSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['phucanh.vn']
    start_urls = [
        'http://phucanh.vn/may-tinh-xach-tay-laptop.html',
        'http://phucanh.vn/may-tinh-bang-tablet.html',
        'http://phucanh.vn/dien-thoai-thong-minh.html',
        'http://phucanh.vn/dien-thoai-di-dong.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://phucanh.vn/may-tinh-xach-tay-laptop.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="paging"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://phucanh.vn/may-tinh-bang-tablet.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="paging"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://phucanh.vn/dien-thoai-thong-minh.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="paging"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://phucanh.vn/dien-thoai-di-dong.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="paging"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="pro_item relative "]//div[@class="pro_sum absolute"]/a/@href',
        'source' : 'phucanh.vn',
        'title' : '//*[@class="product_detail_top"]//h1[@class="product_name"]//text()',
        'price' : '//*[@class="box_info"]//div[@class="product_price"]//text()'
    }