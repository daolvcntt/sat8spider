# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class FamSpider(AbstractPriceSpider):

    allowed_domains = ['fam.vn']

    start_urls = [
        'http://fam.vn/vn/MÁY-TÍNH-XÁCH-TAY-p1001',
        'http://fam.vn/vn/Máy-tính-bảng-p1573'
    ]

    rules = (
        Rule (LinkExtractor(allow=('type.php\?module=product\&iCat=1001\&page=[0-9]+'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product"]//div[@class="pic"]/a[1]/@href',
        'source' : 'fam.vn',
        'title' : '//*[@class="pro_detail"]//td[@class="pro_name"]//text()',
        'price' : '//*[@id="table1"]//td[@valign="bottom"]//span[1]/text()'
    }