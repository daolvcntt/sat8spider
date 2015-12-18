# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class TikiSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['tiki.vn']
	start_urls = [
		'http://tiki.vn/dien-thoai-di-dong/c1793',
		'http://tiki.vn/dien-thoai-may-tinh-bang/c1789/',
		'http://tiki.vn/may-tinh-bang/c1794'
	]
	rules = (
	  	Rule (LinkExtractor(allow=('http://tiki.vn/dien-thoai-di-dong/c1793\?page=[0-9]+')), callback='parse_item', follow= True),
	  	Rule (LinkExtractor(allow=('http://tiki.vn/dien-thoai-may-tinh-bang/c1789/\?page=[0-9]+')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="product-item "]/a/@href',
		'source' : 'tiki.vn',
		'title' : '//*[@class="item-box"]/h1[@class="item-name"]/text()',
		'price' : '//*[@id="span-price"]/text()'
	}