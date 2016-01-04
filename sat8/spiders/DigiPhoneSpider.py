# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DigiPhoneSpider(AbstractPriceSpider):
	allowed_domains = ['digiphone.com.vn', ]

	start_urls = [
	    'http://digiphone.com.vn/dien-thoai/',
	    'http://digiphone.com.vn/may-tinh-bang/'
	]

	rules = (
	    Rule (LinkExtractor(allow=('http://digiphone.com.vn/dien-thoai/\&p=[0-9]'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="xemchitiet_sp"]/@href',
		'source' : 'digiphone.com.vn',
		'title' : '//*[@class="name_product"]/text()',
		'price' : '//*[@class="giagiam"]/text()'
	}