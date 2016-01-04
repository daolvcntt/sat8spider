# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

from scrapy.selector import Selector
import json,urllib

class NguyenKimLaptopPriceSpider(AbstractPriceSpider):
    allowed_domains = ["www.nguyenkim.com"]
    start_urls = [
        'http://www.nguyenkim.com/may-tinh-xach-tay/',
    ]
    rules = (
        Rule (LinkExtractor(allow=('http://www.nguyenkim.com/index.php\?dispatch=categories.load\&category_id=527\&next_page=[0-9]+\&columns=4\&get_more=y\&features_hash=\&items_per_page=20\&sort_by=popularity\&sort_order=desc\&result_ids=gird-scroll-page')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="ty-grid-list__image"]/a[1]/@href',
        'source' : 'www.nguyenkim.com',
        'title' : '//*[@class="block_product-title"]/text()',
        'price' : '//*[@class="actual-price "]//span[@class="price-num"]/text()'
    }