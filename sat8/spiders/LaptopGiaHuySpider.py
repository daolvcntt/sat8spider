# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class LaptopGiaHuySpider(AbstractPriceSpider):
    allowed_domains = ['laptopgiahuy.vn']
    start_urls = [
        'http://laptopgiahuy.vn/dien-thoai-di-dong.html',
        'http://laptopgiahuy.vn/may-tinh-bang.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://laptopgiahuy.vn/dien-thoai-di-dong-pi=[0-9]+.html'), restrict_xpaths=('//div[@class="Paging PagingReview"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://laptopgiahuy.vn/may-tinh-bang-pi=[0-9]+.html'), restrict_xpaths=('//div[@class="Paging PagingReview"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="Home-Product text-center col-xs-12 col-sm-6 col-md-4 col-lg-3"]/@href',
        'source' : 'laptopgiahuy.vn',
        'title' : '//*[@class="ProductNameLink ProductNameLinkDetail"]//text()',
        'price' : '//*[@class="ProductPriceNew clearfix"]//text()'
    }