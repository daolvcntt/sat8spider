# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DiDongProSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['didong.pro']
	start_urls = [
		'http://didong.pro/dien-thoai-di-dong',
	]

	rules = (
	  	Rule (LinkExtractor(allow=('http://didong.pro/dien-thoai-di-dong\?page=[0-9]+')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="name"]/a/@href',
		'source' : 'didong.pro',
		'title' : '//*[@class="extra-wrap"]/h1//text()',
		'price' : '//*[@class="price-new"]//text()'
	}