# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class CdiscountSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['www.cdiscount.vn']
    start_urls = [
        'http://www.cdiscount.vn/cong-nghe/thiet-bi-van-phong/laptop/l-26030406.html#_his_',
        'http://www.cdiscount.vn/cong-nghe/dien-thoai-phu-kien/dien-thoai/smartphone/l-2603010100.html#_his_',
        'http://www.cdiscount.vn/cong-nghe/may-tinh-bang-phu-kien/may-tinh-bang/l-26030000.html#_his_'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://www.cdiscount.vn/cong-nghe/thiet-bi-van-phong/laptop/l-26030406\-[0-9]+.html'), restrict_xpaths=('//div[@class="pgWrap"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.cdiscount.vn/cong-nghe/dien-thoai-phu-kien/dien-thoai/smartphone/l-2603010100\-[0-9]+.html'), restrict_xpaths=('//div[@class="pgWrap"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.cdiscount.vn/cong-nghe/may-tinh-bang-phu-kien/may-tinh-bang/l-26030000\-[0-9]+.html'), restrict_xpaths=('//div[@class="pgWrap"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@id="lpBloc"]/li//a[1]/@href',
        'source' : 'www.cdiscount.vn',
        'title' : '//h1//text()',
        'price' : '//*[@class="fpPrice price"]//text()'
    }