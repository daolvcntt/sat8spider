# -*- coding: utf-8 -*-
# Chua xong
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class HcSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['hc.com.vn']
	start_urls = [
		'http://hc.com.vn/dien-thoai/dien-thoai-di-dong',
	]
	rules = (
	  	Rule (LinkExtractor(allow=('http://hc.com.vn/dien-thoai/dien-thoai-di-dong\?p=[0-9]+')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="product-name"]/a/@href',
		'source' : 'hc.com.vn',
		'title' : '//*[@class="product-name"]/h1//text()',
		'price' : '//*[@class="price"]//text()'
	}