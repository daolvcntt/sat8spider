# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class NhatCuongMobileSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['www.adayroi.com']
	start_urls = [
		'https://www.adayroi.com/dien-thoai-may-tinh-bang-m322',
		'https://www.adayroi.com/laptop-m350'
	]

	rules = (
		Rule (LinkExtractor(allow=('http://www.adayroi.com/dien-thoai-may-tinh-bang-m322\?p=[0-9]+'), restrict_xpaths=('//div[@class="adr pagination"]')), callback='parse_item', follow= True),
		Rule (LinkExtractor(allow=('http://www.adayroi.com/laptop-m350\?p=[0-9]+'), restrict_xpaths=('//div[@class="adr pagination"]')), callback='parse_item', follow= True),
	)