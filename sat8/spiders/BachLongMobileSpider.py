# -*- coding: utf-8 -*-
# Chua xong
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class BachLongMobileSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['bachlongmobile.com']
	start_urls = [
		'http://bachlongmobile.com/dien-thoai.html',
		'http://bachlongmobile.com/may-tinh-bang.html'
	]
	rules = (
	  	Rule (LinkExtractor(allow=('http://www.hnammobile.com/dien-thoai/\?p=[0-9]+#ds')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="pitem"]/a[@class="product-item"]/@href',
		'source' : 'bachlongmobile.com',
		'title' : '//*[@id="product-detail"]/h2[1]/text()',
		'price' : '//*[@id="product-detail"]/div[2]/span[1]'
	}