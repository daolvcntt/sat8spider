# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class TikiSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['www.techone.vn']
	start_urls = [
		'http://www.techone.vn/dien-thoai/',
		'http://www.techone.vn/may-tinh-bang/'
	]
	rules = (
	  	Rule (LinkExtractor(allow=('http://www.techone.vn/dien-thoai/\&page=[0-9]+')), callback='parse_item', follow= True),
	  	Rule (LinkExtractor(allow=('http://www.techone.vn/may-tinh-bang/\&page=[0-9]+')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="lmhref"]/@href',
		'source' : 'techone.vn',
		'title' : '//*[@class="ptitle"]/h1/text()',
		'price' : '//*[@class="pprice"]/span[@class="price"]/text()'
	}