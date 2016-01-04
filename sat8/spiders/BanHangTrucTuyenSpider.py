# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class BanHangTrucTuyenSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['banhangtructuyen.vn']
	start_urls = [
		'https://banhangtructuyen.vn/dien-thoai-di-dong.html',
		'https://banhangtructuyen.vn/may-tinh-bang.html'
	]
	rules = (
	  	Rule (LinkExtractor(allow=('https://banhangtructuyen.vn/dien-thoai-di-dong-page-[0-9]+.html')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="cm-gallery-item cm-item-gallery"]/a/@href',
		'source' : 'banhangtructuyen.vn',
		'title' : '//*[@class="ty-product-block-title"]//text()',
		'price' : '//*[@class="ty-price"]/span[1]//text()'
	}