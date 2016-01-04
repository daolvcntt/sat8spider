# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class PicoSpider(AbstractPriceSpider):
    allowed_domains = ['pico.vn', ]
    start_urls = ['http://pico.vn/may-tinh-xach-tay-nhom-58.html', ]
    rules = (
        Rule (LinkExtractor(allow=('may-tinh-xach-tay-nhom-58.html\?&\pageIndex=[0-9]+'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product-info"]/h6/a/@href',
        'source' : 'pico.vn',
        'title' : '//*[@id="Home_ContentPlaceHolder_Product_Control_head_Title"]/text()',
        'price' : '//*[@class="sidebar-box-content sidebar-padding-box product-single-info "]/span[@class="price"]/text()'
    }