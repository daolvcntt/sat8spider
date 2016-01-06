# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class Yes24Spider(AbstractPriceSpider):
    allowed_domains = ['www.yes24.vn']
    start_urls = [
        'http://www.yes24.vn/Display/Item/NewItem2nd.aspx?FCategoryNo=480570&SCategoryNo=480590',
        'http://www.yes24.vn/Display/Item/NewItem2nd.aspx?FCategoryNo=480570&SCategoryNo=480580',
        'http://www.yes24.vn/yes24vina/dien-thoai'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://www.yes24.vn/Display/Item/NewItem2nd.aspx\?FCategoryNo=480570\&SCategoryNo=480590\&currentPage=[0-9]+\#ListTop'), restrict_xpaths=('//div[@id="ctl00_ContentPlaceHolder2_pnItemProductList"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.yes24.vn/Display/Item/NewItem2nd.aspx\?FCategoryNo=480570\&SCategoryNo=480580\&currentPage=[0-9]+\#ListTop'), restrict_xpaths=('//div[@id="ctl00_ContentPlaceHolder2_pnItemProductList"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="listItem"]//a[1]/@href',
        'source' : 'www.yes24.vn',
        'title' : '//*[@class="prodMobileSummaryWrap"]//h1[1]/text()',
        'price' : '//*[@id="ctl00_ContentPlaceHolder2_ctl00_lblSalePrice"]/text() | //*[@id="ctl00_ContentPlaceHolder2_ctl01_lblSalePrice"]/text()'
    }