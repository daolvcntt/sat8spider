# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DienMayThienHoaSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['www.dienmaythienhoa.vn']
	start_urls = [
		'http://www.dienmaythienhoa.vn/vien-thong.html',
	]
	rules = (
	  	Rule (LinkExtractor(allow=('http://www.dienmaythienhoa.vn/vien-thong-page-[0-9]+.html')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="product-title"]/@href',
		'source' : 'www.dienmaythienhoa.vn',
		'title' : '//*[@class="mainbox-title"]//text()',
		'price' : '//*[@class="actual-price "]/span[1]//text()'
	}