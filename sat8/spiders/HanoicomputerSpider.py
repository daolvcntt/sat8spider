# -*- coding: utf-8 -*-

import scrapy
import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

from scrapy.selector import Selector
from sat8.items import ProductPriceItem, ProductItemLoader
from urlparse import urlparse
from time import gmtime, strftime

class HanoicomputerSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['www.hanoicomputer.vn']
    start_urls = [
        'http://www.hanoicomputer.vn/laptop/c3.html',
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://www.hanoicomputer.vn/laptop/c3.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="paging"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="product_list page_inside"]//a[@class="p_img"]/@href',
        'source' : 'www.hanoicomputer.vn',
        'title' : '//*[@id="product_detail"]//h1[1]//text()',
        'price' : '//*[@id="price_deal_detail_2"]//div[@class="img_price_full"]//text()'
    }
