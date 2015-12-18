# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class HoangHaSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['hoanghamobile.com', ]
	start_urls = [
		'https://hoanghamobile.com/dien-thoai-di-dong-c14.html',
		'https://hoanghamobile.com/may-tinh-bang-c9.html',
		'https://hoanghamobile.com/may-tinh-xach-tay-c16.html'
	]
	rules = (
		Rule (LinkExtractor(allow=('dien-thoai-di-dong-c14.html\?sort=[0-9]+&p=[0-9]+'), restrict_xpaths=('//div[@class="paging"]')), callback='parse_item', follow= True),
		Rule (LinkExtractor(allow=('may-tinh-bang-c9.html\?sort=[0-9]+&p=[0-9]+'), restrict_xpaths=('//div[@class="paging"]')), callback='parse_item', follow= True),
		Rule (LinkExtractor(allow=('may-tinh-xach-tay-c16.html\?sort=[0-9]+&p=[0-9]+'), restrict_xpaths=('//div[@class="paging"]')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="mosaic-overlay"]/@href',
		'source' : 'hoanghamobile.com',
		'title' : '//*[@class="product-details"]//h1[1]/strong/text()',
		'price' : '//*[@class="product-price"]/p/span/text()'
	}