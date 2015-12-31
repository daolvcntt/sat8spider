# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DienMayChoLonSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['dienmaycholon.vn']
    start_urls = [
        'http://dienmaycholon.vn/danh-muc/44/laptop',
        'http://dienmaycholon.vn/danh-muc/13/dien-thoai-di-dong',
        'http://dienmaycholon.vn/danh-muc/42/may-tinh-bang'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://dienmaycholon.vn/danh-muc/44/laptop/[0-9]+'), restrict_xpaths=('//ul[@class="paging-nav cate"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://dienmaycholon.vn/danh-muc/13/dien-thoai-di-dong/[0-9]+'), restrict_xpaths=('//ul[@class="paging-nav cate"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://dienmaycholon.vn/danh-muc/42/may-tinh-bang/[0-9]+'), restrict_xpaths=('//ul[@class="paging-nav cate"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product-item clearfix"]//a[1]/@href',
        'source' : 'dienmaycholon.vn',
        'title' : '//*[@class="product-title"]//text()',
        'price' : '//*[@class="price-info"]//strong[@class="tag-red"]//text()'
    }