# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class TheGioiTraGopSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['thegioitragop.vn']
	start_urls = [
		'http://thegioitragop.vn/mua-tra-gop-dien-thoai.html',
		'http://thegioitragop.vn/mua-tra-gop-may-tinh-bang.html',
		'http://thegioitragop.vn/mua-tra-gop-laptop.html'
	]
	rules = (
	  	Rule (LinkExtractor(allow=('http://thegioitragop.vn/mua-tra-gop-dien-thoai.html/\?p=[0-9]+')), callback='parse_item', follow= True),
	  	Rule (LinkExtractor(allow=('http://thegioitragop.vn/mua-tra-gop-may-tinh-bang.html/\?p=[0-9]+')), callback='parse_item', follow= True),
	  	Rule (LinkExtractor(allow=('http://thegioitragop.vn/mua-tra-gop-laptop.html/\?p=[0-9]+')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="item-view view1 clearfix"]/div/a/@href',
		'source' : 'thegioitragop.vn',
		'title' : '//*[@class="p_name"]//text()',
		'price' : '//*[@class="price"]//text()'
	}