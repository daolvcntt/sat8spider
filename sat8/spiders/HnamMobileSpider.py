# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class HnamMobileSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['www.hnammobile.com']
	start_urls = [
		'http://www.hnammobile.com/dien-thoai/',
		'http://www.hnammobile.com/may-tinh-bang/',
		'http://www.hnammobile.com/laptop/apple.html'
	]
	rules = (
	  	Rule (LinkExtractor(allow=('http://www.hnammobile.com/dien-thoai/\?p=[0-9]+#ds')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="pitem"]/a[@class="product-item"]/@href',
		'source' : 'hnammobile.com',
		'title' : '//*[@id="product-detail"]/h2[1]/text()',
		'price' : '//*[@id="product-detail"]/div[2]/span[1]'
	}