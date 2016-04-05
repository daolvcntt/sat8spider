# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class BachKhoaShopSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['www.bachkhoashop.com']
	start_urls = [
		'http://www.bachkhoashop.com/dtdd.html',
		'http://www.bachkhoashop.com/may-tinh-bang.html',
		'http://www.bachkhoashop.com/laptop.html'
	]

	rules = (
		Rule (LinkExtractor(allow=('http://www.bachkhoashop.com/dtdd.html\?page=[0-9]+&sort=sort_order&order=ASC'), restrict_xpaths=('//p[@class="pagination"]')), callback='parse_item', follow= True),
		Rule (LinkExtractor(allow=('http://www.bachkhoashop.com/may-tinh-bang.html\?page=[0-9]+&sort=sort_order&order=ASC'), restrict_xpaths=('//p[@class="pagination"]')), callback='parse_item', follow= True),
		Rule (LinkExtractor(allow=('http://www.bachkhoashop.com/laptop.html\?page=[0-9]+'), restrict_xpaths=('//p[@class="pagination"]')), callback='parse_item', follow= True),
	)

	# def parse(self, response):
	# 	return self.parse_item(response)

	configs = {
		'product_links' : '//*[@class="listproduct"]/a/@href',
		'source' : 'www.bachkhoashop.com',
		'title' : '//*[@class="wrap-content"]/h1/span[1]/text()',
		'price' : '//*[@class="pricesell"]/text()'
	}